"""
ИИ-Репетитор: Прямая работа с Groq API.
Теперь с поддержкой ГОЛОСОВЫХ СООБЩЕНИЙ!
"""

import aiohttp
import io
import os
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.menu import get_tutor_exit_keyboard
from config import HTTP_TIMEOUT

router = Router()

API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = "llama-3.1-8b-instant"  
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_WHISPER_URL = "https://api.groq.com/openai/v1/audio/transcriptions"

class TutorState(StatesGroup):
    chatting = State()

SYSTEM_PROMPT = """
Ты — дружелюбный репетитор японского языка по имени Акира.
Ты общаешься с учеником в Telegram. Уровень ученика: начинающий (JLPT N5).

Твои правила:
1. Пиши короткие, простые предложения на японском.
2. ВСЕГДА добавляй транскрипцию (ромадзи) и перевод на русский в скобках.
3. Если ученик делает ошибку, мягко поправь его и объясни правило.
4. Задавай вопросы, чтобы поддерживать диалог.
"""

# Убрали кастомный SSL-контекст, используем системный
async def ask_groq_api(history: list) -> str:
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    payload = {"model": MODEL_NAME, "messages": history, "temperature": 0.7, "max_tokens": 250}
    timeout = aiohttp.ClientTimeout(total=HTTP_TIMEOUT)
    
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.post(GROQ_API_URL, headers=headers, json=payload) as response:
            if response.status == 200:
                data = await response.json()
                return data["choices"][0]["message"]["content"]
            else:
                raise Exception(f"HTTP {response.status}: {await response.text()}")

async def transcribe_audio(audio_bytes: bytes) -> str:
    """Отправляет аудио в Whisper (Groq) для перевода в текст."""
    headers = {"Authorization": f"Bearer {API_KEY}"}
    data = aiohttp.FormData()
    data.add_field('file', audio_bytes, filename='voice.ogg', content_type='audio/ogg')
    data.add_field('model', 'whisper-large-v3-turbo')
    
    timeout = aiohttp.ClientTimeout(total=HTTP_TIMEOUT)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.post(GROQ_WHISPER_URL, headers=headers, data=data) as response:
            if response.status == 200:
                res = await response.json()
                return res.get("text", "")
            else:
                raise Exception(f"Audio Error: {await response.text()}")

@router.callback_query(F.data == "menu:tutor")
async def start_tutor_chat(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(TutorState.chatting)
    await state.update_data(chat_history=[{"role": "system", "content": SYSTEM_PROMPT}])
    
    welcome_text = (
        "🗣️ **Чат с Сенсеем Акирой**\n\n"
        "Напиши текст **или отправь голосовое сообщение**! "
        "Акира умеет слушать.\n\nПопробуй сказать `Привет` или `Konnichiwa`."
    )
    try: await callback.message.delete()
    except: pass
    await callback.message.answer(welcome_text, reply_markup=get_tutor_exit_keyboard())


@router.message(TutorState.chatting, F.voice)
async def handle_tutor_voice(message: Message, state: FSMContext):
    """Обрабатывает ГОЛОСОВЫЕ сообщения от ученика."""
    await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")
    
    # 1. Скачиваем голосовое
    file_id = message.voice.file_id
    file = await message.bot.get_file(file_id)
    file_io = io.BytesIO()
    await message.bot.download_file(file.file_path, destination=file_io)
    
    # 2. Переводим в текст
    try:
        user_text = await transcribe_audio(file_io.getvalue())
        if not user_text.strip():
            return await message.answer("Тишина... Не смог расслышать 😔 Попробуй еще раз!", reply_markup=get_tutor_exit_keyboard())
            
        # Показываем ученику, что бот услышал
        await message.answer(f"🎙 _Вы сказали:_ {user_text}", parse_mode="Markdown")
    except Exception as e:
        print(e)
        return await message.answer("Ошибка распознавания голоса. Напиши текстом!", reply_markup=get_tutor_exit_keyboard())
        
    # 3. Отправляем текст в LLM
    await process_llm_request(message, state, user_text)


@router.message(TutorState.chatting, F.text)
async def handle_tutor_message(message: Message, state: FSMContext):
    """Обрабатывает ТЕКСТОВЫЕ сообщения."""
    await process_llm_request(message, state, message.text)


async def process_llm_request(message: Message, state: FSMContext, user_text: str):
    await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")
    data = await state.get_data()
    history = data.get("chat_history", [{"role": "system", "content": SYSTEM_PROMPT}])
    history.append({"role": "user", "content": user_text})
    
    try:
        bot_reply = await ask_groq_api(history)
        history.append({"role": "assistant", "content": bot_reply})
        if len(history) > 11: history = [history[0]] + history[-10:]
        await state.update_data(chat_history=history)
        await message.answer(bot_reply, reply_markup=get_tutor_exit_keyboard())
    except Exception as e:
        print(f"LLM Error: {e}")
        await message.answer("Сенсей Акира сейчас отдыхает 😔", reply_markup=get_tutor_exit_keyboard())