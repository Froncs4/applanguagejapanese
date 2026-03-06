"""
Квиз — тесты по группам, Грамматика, Адаптивный Микс и Еженедельные квесты.
"""

import random
import asyncio
import time
from datetime import datetime
from aiogram import Router, F
from aiogram.types import CallbackQuery, BufferedInputFile, InputMediaPhoto, Message
from aiogram.fsm.context import FSMContext

from data.content import get_content, get_groups, SIMILAR_CHARS
from database import (
    get_or_create_user, add_xp, update_streak, add_daily_progress, 
    update_blitz_score, get_weakest_cards, update_stats_and_achievements
)
from srs import process_answer
from keyboards.quiz import get_quiz_keyboard, get_result_keyboard, QuizStates
from config import QUIZ_OPTIONS_COUNT, XP_CORRECT, XP_STREAK_BONUS, STREAK_BONUS_EVERY, PENALTY_QUEUE_SIZE
from images import create_quiz_card, create_result_card

router = Router()

async def send_quiz_card(callback: CallbackQuery, card_type: str, action: str, group_key: str, state: FSMContext):
    await state.update_data(card_type=card_type, group_key=group_key, action=action)
    actual_type = card_type
    user_id = callback.from_user.id
    
    is_audio = (card_type == "audio_quiz")
    is_blitz = (card_type == "blitz")
    is_adaptive = (card_type == "mixed")
    
    if is_audio or is_blitz:
        actual_type = random.choice(["hiragana", "katakana", "kanji_n5", "words_n5"])
    elif card_type == "n5_mixed": 
        actual_type = random.choice(["kanji_n5", "words_n5", "grammar_n5"])
    elif card_type == "n4_mixed": 
        actual_type = random.choice(["kanji_n4", "words_n4"])
        
    # === СИСТЕМА УМНЫХ ПОВТОРОВ (ШТРАФНОЙ КРУГ) ===
    state_data = await state.get_data()
    penalty_queue = state_data.get('penalty_queue', [])
    use_penalty = False
    
    valid_penalties = [p for p in penalty_queue if p['type'] == actual_type or is_adaptive or is_blitz]
    
    # С вероятностью 40% выдаем ошибку снова
    if valid_penalties and random.random() < 0.4:
        penalty_item = valid_penalties[0]
        penalty_queue.remove(penalty_item)
        await state.update_data(penalty_queue=penalty_queue)
        
        actual_type = penalty_item['type']
        question_key = penalty_item['key']
        quiz_content = get_content(actual_type)
        correct_answer = quiz_content.get(question_key)
        contexts = []
        use_penalty = True
        
    if not use_penalty:
        if is_adaptive:
            actual_type = random.choice(["hiragana", "katakana", "kanji_n5", "words_n5", "kanji_n4", "words_n4"])
            weak_cards = await get_weakest_cards(user_id, actual_type, limit=5)
            all_content = get_content(actual_type)
            question_key = random.choice(weak_cards) if weak_cards else random.choice(list(all_content.keys()))
            correct_answer = all_content.get(question_key)
            quiz_content, contexts = all_content, []
        else:
            if group_key:
                groups = get_groups(actual_type)
                group = groups.get(group_key)
                if not group:
                    quiz_content, contexts = get_content(actual_type), []
                else:
                    quiz_content, contexts = dict(zip(group["chars"], group["readings"])), group.get("contexts", [])
            else:
                quiz_content, contexts = get_content(actual_type), []
            
            if not quiz_content: return await callback.message.answer("Нет данных для этого раздела.")
            all_keys = list(quiz_content.keys())
            question_key = random.choice(all_keys)
            correct_answer = quiz_content[question_key]
        
    context_text = None
    if contexts and not is_adaptive and not use_penalty and question_key in list(quiz_content.keys()):
        idx = list(quiz_content.keys()).index(question_key)
        if idx < len(contexts): context_text = contexts[idx]

    # === ЛОВУШКИ ===
    all_content = get_content(actual_type)
    wrong_pool = []
    
    if question_key in SIMILAR_CHARS:
        for trap_char in SIMILAR_CHARS[question_key]:
            if trap_char in all_content:
                wrong_pool.append(all_content[trap_char])
                
    remaining_wrong = [v for k, v in all_content.items() if v != correct_answer and v not in wrong_pool]
    num_needed = min(QUIZ_OPTIONS_COUNT - 1, len(wrong_pool) + len(remaining_wrong))
    
    if len(wrong_pool) >= num_needed: wrong_answers = wrong_pool[:num_needed]
    else: wrong_answers = wrong_pool + random.sample(remaining_wrong, num_needed - len(wrong_pool))

    options = wrong_answers + [correct_answer]
    random.shuffle(options)
    correct_index = options.index(correct_answer)

    from ui import create_quiz_message
    caption = create_quiz_message(card_type, question_key, context=context_text)
    
    card_image = await asyncio.to_thread(create_quiz_card, question_key, actual_type)
    keyboard = get_quiz_keyboard(options, correct_index, actual_type, question_key)

    if is_audio:
        from audio import generate_japanese_voice
        try:
            audio_bytes = await asyncio.to_thread(generate_japanese_voice, question_key)
            await callback.message.answer_voice(voice=BufferedInputFile(audio_bytes, filename="audio.ogg"), caption="Слушай внимательно!")
        except: pass

    try:
        await callback.message.edit_media(media=InputMediaPhoto(media=BufferedInputFile(card_image, filename="quiz.png"), caption=caption), reply_markup=keyboard)
    except:
        try: await callback.message.delete()
        except: pass
        await callback.message.answer_photo(photo=BufferedInputFile(card_image, filename="quiz.png"), caption=caption, reply_markup=keyboard)


# ==========================================
# ОБЩАЯ ФУНКЦИЯ ОБРАБОТКИ ОТВЕТОВ
# ==========================================
async def process_answer_logic(event, state: FSMContext, card_type: str, card_key: str, correct_text: str, correct: bool):
    user_id = event.from_user.id
    
    if not correct:
        state_data = await state.get_data()
        penalty_queue = state_data.get('penalty_queue', [])
        # Добавляем карточку в очередь, но ограничиваем размер
        penalty_queue.append({'key': card_key, 'type': card_type})
        if len(penalty_queue) > PENALTY_QUEUE_SIZE:
            penalty_queue.pop(0)  # удаляем самый старый
        await state.update_data(penalty_queue=penalty_queue)
    else:
        # Если ответ правильный, удаляем эту карточку из очереди (если она там есть)
        state_data = await state.get_data()
        penalty_queue = state_data.get('penalty_queue', [])
        penalty_queue = [p for p in penalty_queue if not (p['key'] == card_key and p['type'] == card_type)]
        await state.update_data(penalty_queue=penalty_queue)
        
    await process_answer(user_id, card_type, card_key, correct)
    streak_data = await update_streak(user_id, correct)

    xp_gained = 0
    if correct:
        xp_gained = XP_CORRECT + (XP_STREAK_BONUS if streak_data["current_streak"] % STREAK_BONUS_EVERY == 0 else 0)
        await add_xp(user_id, xp_gained)
        prog, goal, just_done_daily, just_done_weekly = await add_daily_progress(user_id)
        
        if just_done_daily:
            await add_xp(user_id, 50)
            msg = "🎉 **ЕЖЕДНЕВНАЯ ЦЕЛЬ ВЫПОЛНЕНА!** +50 XP!"
            if isinstance(event, Message): await event.answer(msg)
            else: await event.message.answer(msg)
            
        if just_done_weekly:
            await add_xp(user_id, 500)
            msg = "🏆 **ЕЖЕНЕДЕЛЬНЫЙ КВЕСТ ВЫПОЛНЕН!** Невероятно! +500 XP!"
            if isinstance(event, Message): await event.answer(msg)
            else: await event.message.answer(msg)
            
        now_hour = datetime.now().hour
        is_night = (0 <= now_hour < 4)
        is_grammar = (card_type == "grammar_n5")
        if is_night or is_grammar:
            await update_stats_and_achievements(user_id, is_grammar_perfect=is_grammar, is_night=is_night)

    res_img = await asyncio.to_thread(create_result_card, correct, card_key, correct_text, xp_gained, streak_data['current_streak'])
    keyboard = get_result_keyboard(card_type, "learn", correct, (await state.get_data()).get("group_key"))
    
    if isinstance(event, Message):
        await state.clear()
        await event.answer_photo(photo=BufferedInputFile(res_img, filename="res.png"), reply_markup=keyboard)
    else:
        try:
            await event.message.edit_media(
                media=InputMediaPhoto(media=BufferedInputFile(res_img, filename="res.png")), 
                reply_markup=keyboard
            )
        except:
            try: await event.message.delete()
            except: pass
            await event.message.answer_photo(photo=BufferedInputFile(res_img, filename="res.png"), reply_markup=keyboard)


# ==========================================
# ХЕНДЛЕРЫ КНОПОК
# ==========================================
@router.callback_query(F.data.startswith("mode:"))
async def on_mode_selected(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    parts = callback.data.split(":")
    await get_or_create_user(callback.from_user.id)
    await send_quiz_card(callback, parts[2], parts[1], None, state)


@router.callback_query(F.data.startswith("quiz_group:"))
async def on_quiz_group(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    parts = callback.data.split(":")
    await get_or_create_user(callback.from_user.id)
    await send_quiz_card(callback, parts[1], "learn", parts[2], state)


@router.callback_query(F.data == "start_blitz")
async def start_blitz(callback: CallbackQuery, state: FSMContext):
    await callback.answer("🚀 Блиц начинается!")
    await state.update_data(blitz_end_time=time.time() + 60, blitz_score=0)
    await state.set_state(QuizStates.blitz_mode)
    await send_quiz_card(callback, "blitz", "learn", None, state)


@router.callback_query(F.data.startswith("type_answer:"))
async def on_type_answer(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    parts = callback.data.split(":")
    buttons = callback.message.reply_markup.inline_keyboard
    correct_text = buttons[int(parts[3])][0].text.split(". ", 1)[1] if ". " in buttons[int(parts[3])][0].text else buttons[int(parts[3])][0].text
    await state.update_data(card_type=parts[1], card_key=parts[2], correct_text=correct_text, quiz_msg_id=callback.message.message_id)
    await state.set_state(QuizStates.typing_answer)
    await callback.message.answer("⌨️ Введи правильный ответ (на русском или ромадзи):")


@router.message(QuizStates.typing_answer)
async def process_typed_answer(message: Message, state: FSMContext):
    user_data = await state.get_data()
    correct_text = user_data.get("correct_text", "").lower().strip()
    user_answer = message.text.lower().strip()
    correct = (user_answer == correct_text) or (user_answer in correct_text and len(user_answer) > 2)
    
    await process_answer_logic(message, state, user_data.get("card_type"), user_data.get("card_key"), correct_text, correct)


@router.callback_query(F.data.startswith("answer:"))
async def on_answer(callback: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state == QuizStates.typing_answer: await state.set_state(None)
        
    await callback.answer()
    parts = callback.data.split(":")
    card_type, card_key, selected_index, correct_index = parts[1], parts[2], int(parts[3]), int(parts[4])
    correct = (selected_index == correct_index)
    user_id = callback.from_user.id
    
    if current_state == QuizStates.blitz_mode:
        data = await state.get_data()
        if time.time() > data.get("blitz_end_time", 0):
            score = data.get("blitz_score", 0) + (1 if correct else 0)
            is_new_record = await update_blitz_score(user_id, score)
            await state.clear()
            msg = f"⏱ Время вышло!\nТвой результат: **{score}** правильных ответов! 🔥"
            if is_new_record: msg += "\n🏆 ЭТО ТВОЙ НОВЫЙ РЕКОРД!"
            return await callback.message.answer(msg)

        if correct: await state.update_data(blitz_score=data.get("blitz_score", 0) + 1)
        return await send_quiz_card(callback, "blitz", "learn", None, state)

    buttons = callback.message.reply_markup.inline_keyboard
    full_text = buttons[correct_index][0].text
    correct_text = full_text.split(". ", 1)[1] if ". " in full_text else full_text

    await process_answer_logic(callback, state, card_type, card_key, correct_text, correct)


@router.callback_query(F.data.startswith("hint:"))
async def on_hint(callback: CallbackQuery):
    answer = get_content(callback.data.split(":")[1]).get(callback.data.split(":")[2], "???")
    await callback.answer(f"💡 Начинается на: {answer[0] + '...' if len(answer) > 1 else '?'}", show_alert=True)


@router.callback_query(F.data.startswith("skip:"))
async def on_skip(callback: CallbackQuery, state: FSMContext):
    await state.set_state(None)
    await callback.answer("⏭ Пропускаем...")
    user_data = await state.get_data()
    await send_quiz_card(callback, callback.data.split(":")[1] if len(callback.data.split(":")) > 1 else "hiragana", user_data.get("action", "learn"), user_data.get("group_key"), state)


@router.callback_query(F.data.startswith("next:"))
async def on_next_card(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    parts = callback.data.split(":")
    group_key = parts[3] if len(parts) >= 4 and parts[3] else (await state.get_data()).get("group_key")
    await send_quiz_card(callback, parts[2], parts[1], group_key, state)