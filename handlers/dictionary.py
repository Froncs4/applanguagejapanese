"""
Умный карманный словарь: обработка текстовых запросов с Пагинацией.
"""

import asyncio
import re
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, BufferedInputFile
from aiogram.filters import StateFilter

from data.content import HIRAGANA, KATAKANA, KANJI_N5, WORDS_N5, KANJI_N4, WORDS_N4
from images import create_dictionary_card
from audio import generate_japanese_voice
from handlers.study import fetch_gif_bytes

router = Router()

def search_in_dictionary(query: str) -> list:
    query = query.lower().strip()
    results = []
    databases = [
        ("hiragana", HIRAGANA), ("katakana", KATAKANA),
        ("kanji_n5", KANJI_N5), ("words_n5", WORDS_N5),
        ("kanji_n4", KANJI_N4), ("words_n4", WORDS_N4)
    ]
    for db_type, db_content in databases:
        for symbol, reading_translation in db_content.items():
            if query == symbol.lower():
                if not any(r['symbol'] == symbol for r in results): results.append({"type": db_type, "symbol": symbol, "reading": reading_translation})
                continue
            if query in reading_translation.lower():
                if not any(r['symbol'] == symbol for r in results): results.append({"type": db_type, "symbol": symbol, "reading": reading_translation})
                continue
    return results

async def send_dictionary_page(message_or_callback, query: str, found_items: list, page: int):
    # Пагинация: берем по 3 элемента на страницу
    total_pages = (len(found_items) + 2) // 3
    page = max(0, min(page, total_pages - 1))
    
    card_image = await asyncio.to_thread(create_dictionary_card, query, found_items, page)
    
    buttons = []
    if found_items:
        current_items = found_items[page * 3 : (page + 1) * 3]
        for item in current_items:
            row = []
            symbol, c_type = item['symbol'], item['type']
            row.append(InlineKeyboardButton(text=f"🔊 {symbol}", callback_data=f"dict_voice:{symbol}"))
            if not c_type.startswith("words"):
                reading = item['reading'].split()[0] if " " in item['reading'] else item['reading']
                row.append(InlineKeyboardButton(text=f"✍️ Начертание", callback_data=f"dict_gif:{c_type}:{symbol}:{reading}"))
            buttons.append(row)
            
        # Кнопки страниц
        if total_pages > 1:
            nav_row = []
            if page > 0: nav_row.append(InlineKeyboardButton(text="⬅️ Назад", callback_data=f"dict_page:{query}:{page-1}"))
            nav_row.append(InlineKeyboardButton(text=f"{page+1}/{total_pages}", callback_data="noop"))
            if page < total_pages - 1: nav_row.append(InlineKeyboardButton(text="Вперед ➡️", callback_data=f"dict_page:{query}:{page+1}"))
            buttons.append(nav_row)

    buttons.append([InlineKeyboardButton(text="🏠 В главное меню", callback_data="menu:back")])
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    
    if isinstance(message_or_callback, Message):
        await message_or_callback.answer_photo(photo=BufferedInputFile(card_image, filename="dict.png"), reply_markup=kb)
    else:
        try:
            await message_or_callback.message.edit_media(media=InputMediaPhoto(media=BufferedInputFile(card_image, filename="dict.png")), reply_markup=kb)
        except:
            pass

@router.message(StateFilter(None), F.text & ~F.text.startswith("/"))
async def handle_text_search(message: Message):
    query = message.text
    found_items = search_in_dictionary(query)
    await message.bot.send_chat_action(chat_id=message.chat.id, action="upload_photo")
    await send_dictionary_page(message, query, found_items, 0)

@router.callback_query(F.data.startswith("dict_page:"))
async def dict_page_handler(callback: CallbackQuery):
    await callback.answer()
    parts = callback.data.split(":")
    query, page = parts[1], int(parts[2])
    found_items = search_in_dictionary(query)
    await send_dictionary_page(callback, query, found_items, page)

@router.callback_query(F.data.startswith("dict_voice:"))
async def dict_send_voice(callback: CallbackQuery):
    symbol = callback.data.split(":")[1]
    await callback.bot.send_chat_action(chat_id=callback.message.chat.id, action="record_voice")
    audio_bytes = await asyncio.to_thread(generate_japanese_voice, symbol)
    await callback.message.answer_voice(voice=BufferedInputFile(audio_bytes, filename="pron.ogg"), caption=f"🇯🇵 {symbol}")
    await callback.answer()

@router.callback_query(F.data.startswith("dict_gif:"))
async def dict_send_gif(callback: CallbackQuery):
    parts = callback.data.split(":")
    card_type, char, reading = parts[1], parts[2], parts[3].lower()
    
    urls = []
    if card_type in ["hiragana", "katakana"]:
        prefix = card_type.capitalize()
        for v in [reading, reading.replace('shi','si').replace('chi','ti').replace('tsu','tu').replace('fu','hu')]:
            urls.append(f"https://commons.wikimedia.org/wiki/Special:FilePath/{prefix}_{v}_stroke_order_animation.gif")
            urls.append(f"https://commons.wikimedia.org/wiki/Special:FilePath/{prefix}_letter_{v}_stroke_order_animation.gif")
    elif card_type.startswith("kanji"):
        hex_4 = hex(ord(char))[2:].lower()
        hex_5 = hex_4.zfill(5)
        urls.extend([f"https://raw.githubusercontent.com/yagays/kanjivg-gif/master/gifs/{hex_5}.gif", f"https://raw.githubusercontent.com/mistval/kanji_images/master/gifs/{hex_4}.gif"])
        
    await callback.bot.send_chat_action(chat_id=callback.message.chat.id, action="choose_sticker")
    gif_bytes = await fetch_gif_bytes(urls)
    
    if not gif_bytes: return await callback.answer("Анимация недоступна 😔", show_alert=True)
    await callback.message.answer_animation(animation=BufferedInputFile(gif_bytes, filename=f"{char}.gif"), caption=f"✍️ Порядок черт: {char}")
    await callback.answer()
