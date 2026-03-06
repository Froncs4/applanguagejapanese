"""
Режим изучения с озвучкой, GIF-анимациями начертания и авто-очисткой.
"""

import asyncio
import aiohttp
from aiogram import Router, F

from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import BufferedInputFile, InputMediaPhoto
from aiogram.fsm.context import FSMContext

from data.content import get_groups, get_content, get_sorted_groups, MODE_NAMES_RU
from database import get_or_create_user, get_cached_media, set_cached_media
from images import create_study_card, create_groups_card, create_full_table
from audio import generate_japanese_voice
from config import HTTP_TIMEOUT

router = Router()

async def fetch_gif_bytes(urls: list) -> bytes:
    headers = {"User-Agent": "JapaneseLearningBot/1.0 (Educational Telegram Bot)"}
    timeout = aiohttp.ClientTimeout(total=HTTP_TIMEOUT)
    async with aiohttp.ClientSession(timeout=timeout, headers=headers) as session:
        for url in urls:
            try:
                async with session.get(url) as response:
                    if response.status == 200:
                        return await response.read()
            except Exception:
                continue
    return None

async def delete_previous_temp_msg(bot, chat_id: int, state: FSMContext):

    data = await state.get_data()
    temp_msg_id = data.get("temp_msg_id")
    if temp_msg_id:
        try:
            # Проверяем, существует ли сообщение (простейший способ - попытаться удалить)
            await bot.delete_message(chat_id=chat_id, message_id=temp_msg_id)
        except Exception:
            pass
        await state.update_data(temp_msg_id=None)

def get_study_keyboard(card_type: str, group_key: str, index: int, total: int) -> InlineKeyboardMarkup:
    buttons = []
    nav_row = []
    if index > 0: nav_row.append(InlineKeyboardButton(text="«", callback_data=f"study_nav:{card_type}:{group_key}:{index - 1}"))
    else: nav_row.append(InlineKeyboardButton(text=" ", callback_data="noop"))
    nav_row.append(InlineKeyboardButton(text=f"{index + 1} / {total}", callback_data="noop"))
    if index < total - 1: nav_row.append(InlineKeyboardButton(text="»", callback_data=f"study_nav:{card_type}:{group_key}:{index + 1}"))
    else: nav_row.append(InlineKeyboardButton(text=" ", callback_data="noop"))
    buttons.append(nav_row)
    
    quick_nav = []
    if index >= 3: quick_nav.append(InlineKeyboardButton(text="« В начало", callback_data=f"study_nav:{card_type}:{group_key}:0"))
    if index < total - 1: quick_nav.append(InlineKeyboardButton(text="В конец »", callback_data=f"study_nav:{card_type}:{group_key}:{total - 1}"))
    if quick_nav: buttons.append(quick_nav)
        
    interactive_row = [InlineKeyboardButton(text="🔊 Звук", callback_data=f"voice:{card_type}:{group_key}:{index}")]
    if not card_type.startswith("words"): 
        interactive_row.append(InlineKeyboardButton(text="✍️ Начертание", callback_data=f"gif:{card_type}:{group_key}:{index}"))
    buttons.append(interactive_row)
    
    if index == total - 1:
        buttons.append([InlineKeyboardButton(text="✏️ Тест по группе", callback_data=f"quiz_group:{card_type}:{group_key}")])
    
    buttons.append([
        InlineKeyboardButton(text="📚 Группы", callback_data=f"study_groups:{card_type}"),
        InlineKeyboardButton(text="🏠 В меню", callback_data="menu:back"),
    ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


@router.callback_query(F.data == "noop")
async def noop_handler(callback: CallbackQuery):
    await callback.answer()


@router.callback_query(F.data.startswith("study_groups:"))
async def show_groups(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await delete_previous_temp_msg(callback.bot, callback.message.chat.id, state)
    
    card_type = callback.data.split(":", 1)[1]
    groups = get_sorted_groups(card_type)
    
    if not groups: 
        return await callback.message.answer(f"Раздел `{card_type}` пока пуст. Скоро добавим!")
    
    image = await asyncio.to_thread(create_groups_card, card_type, groups)
    
    buttons = []
    for i in range(0, len(groups), 2):
        row = []
        for j in range(2):
            if i + j < len(groups):
                key, group = groups[i + j]
                row.append(InlineKeyboardButton(text=group["name"], callback_data=f"study_group:{card_type}:{key}"))
        buttons.append(row)
    
    buttons.append([InlineKeyboardButton(text="📋 Вся таблица", callback_data=f"study_table:{card_type}")])
    back_target = "menu:alphabet" if card_type in ["hiragana", "katakana"] else "menu:jlpt"
    buttons.append([InlineKeyboardButton(text="« Назад", callback_data=back_target)])
    
    try: await callback.message.delete()
    except: pass
    await callback.message.answer_photo(photo=BufferedInputFile(image, filename="groups.png"), reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))


@router.callback_query(F.data.startswith("study_group:"))
async def start_study_group(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await delete_previous_temp_msg(callback.bot, callback.message.chat.id, state)
    parts = callback.data.split(":")
    card_type, group_key = parts[1], parts[2]
    groups = get_groups(card_type)
    if not groups.get(group_key): return
    await show_study_card(callback, card_type, group_key, 0)


@router.callback_query(F.data.startswith("study_nav:"))
async def navigate_study(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await delete_previous_temp_msg(callback.bot, callback.message.chat.id, state)
    parts = callback.data.split(":")
    card_type, group_key, index = parts[1], parts[2], int(parts[3])
    await show_study_card(callback, card_type, group_key, index)


async def show_study_card(callback: CallbackQuery, card_type: str, group_key: str, index: int):
    groups = get_groups(card_type)
    group = groups.get(group_key)
    if not group or index >= len(group["chars"]): return
    char = group["chars"][index]
    reading = group["readings"][index]
    hint = group["hints"][index] if index < len(group.get("hints", [])) else ""
    audio_hint = group["audio_hints"][index] if index < len(group.get("audio_hints", [])) else ""
    total = len(group["chars"])
    
    card_image = await asyncio.to_thread(
        create_study_card, symbol=char, reading=reading, hint=hint, 
        card_type=card_type, group_name=group["name"], index=index + 1, 
        total=total, audio_hint=audio_hint
    )
    
    keyboard = get_study_keyboard(card_type, group_key, index, total)
    try: await callback.message.edit_media(media=InputMediaPhoto(media=BufferedInputFile(card_image, filename="study.png")), reply_markup=keyboard)
    except:
        try: await callback.message.delete()
        except: pass
        await callback.message.answer_photo(photo=BufferedInputFile(card_image, filename="study.png"), reply_markup=keyboard)


@router.callback_query(F.data.startswith("voice:"))
async def send_voice_pronunciation(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await delete_previous_temp_msg(callback.bot, callback.message.chat.id, state)
    parts = callback.data.split(":")
    card_type, group_key, index = parts[1], parts[2], int(parts[3])
    groups = get_groups(card_type)
    group = groups.get(group_key)
    if not group or index >= len(group["chars"]): return
    char = group["chars"][index]
    
    media_key = f"voice:{char}"
    cached_file_id = await get_cached_media(media_key)
    
    if cached_file_id:
        msg = await callback.message.answer_voice(voice=cached_file_id, caption=f"🇯🇵 Произношение: {char}")
    else:
        await callback.bot.send_chat_action(chat_id=callback.message.chat.id, action="record_voice")
        audio_bytes = await asyncio.to_thread(generate_japanese_voice, char)
        msg = await callback.message.answer_voice(voice=BufferedInputFile(audio_bytes, filename="pronunciation.ogg"), caption=f"🇯🇵 Произношение: {char}")
        await set_cached_media(media_key, msg.voice.file_id, "voice")
        
    await state.update_data(temp_msg_id=msg.message_id)


@router.callback_query(F.data.startswith("gif:"))
async def send_stroke_order_gif(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await delete_previous_temp_msg(callback.bot, callback.message.chat.id, state)
    parts = callback.data.split(":")
    card_type, group_key, index = parts[1], parts[2], int(parts[3])
    groups = get_groups(card_type)
    group = groups.get(group_key)
    if not group or index >= len(group["chars"]): return
    char = group["chars"][index]
    
    media_key = f"gif:{char}"
    cached_file_id = await get_cached_media(media_key)
    
    if cached_file_id:
        msg = await callback.message.answer_animation(animation=cached_file_id, caption=f"✍️ Порядок черт: {char}")
    else:
        reading = group["readings"][index].lower()
        hex_4 = hex(ord(char))[2:].lower()
        hex_5 = hex_4.zfill(5)
        urls = [
            f"https://raw.githubusercontent.com/yagays/kanjivg-gif/master/gifs/{hex_5}.gif",
            f"https://raw.githubusercontent.com/mistval/kanji_images/master/gifs/{hex_4}.gif",
            f"https://raw.githubusercontent.com/yagays/kanjivg-gif/master/gifs/{hex_4}.gif"
        ]
        if card_type in ["hiragana", "katakana"]:
            prefix = card_type.capitalize()
            urls.append(f"https://commons.wikimedia.org/wiki/Special:FilePath/{prefix}_{reading}_stroke_order_animation.gif")
            urls.append(f"https://commons.wikimedia.org/wiki/Special:FilePath/{prefix}_letter_{reading}_stroke_order_animation.gif")
        
        await callback.bot.send_chat_action(chat_id=callback.message.chat.id, action="choose_sticker")
        gif_bytes = await fetch_gif_bytes(urls)
        if not gif_bytes: return await callback.message.answer("Анимация пока недоступна 😔")
        
        msg = await callback.message.answer_animation(animation=BufferedInputFile(gif_bytes, filename=f"{char}.gif"), caption=f"✍️ Порядок черт: {char}")
        await set_cached_media(media_key, msg.animation.file_id, "animation")
        
    await state.update_data(temp_msg_id=msg.message_id)


@router.callback_query(F.data.startswith("study_table:"))
async def show_table(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await delete_previous_temp_msg(callback.bot, callback.message.chat.id, state)
    card_type = callback.data.split(":")[1]
    content = get_content(card_type)
    title = MODE_NAMES_RU.get(card_type, card_type)
    
    image = await asyncio.to_thread(create_full_table, card_type, list(content.keys()), list(content.values()), title=title)
    
    buttons = [[InlineKeyboardButton(text="📚 По группам", callback_data=f"study_groups:{card_type}")]]
    back_target = "menu:alphabet" if card_type in ["hiragana", "katakana"] else "menu:jlpt"
    buttons.append([InlineKeyboardButton(text="« Назад", callback_data=back_target)])
    try: await callback.message.delete()
    except: pass
    await callback.message.answer_photo(photo=BufferedInputFile(image, filename="table.png"), reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))