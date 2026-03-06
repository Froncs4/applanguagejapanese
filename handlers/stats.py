"""
Статистика и красивый Лидерборд с вкладками и Аватарками.
"""

import io
import asyncio
from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import BufferedInputFile

from database import get_user_stats, get_top_players, get_top_blitz
from ui import get_level_info
from images import create_stats_card, create_leaderboard_card

router = Router()

async def fetch_avatar(bot, user_id: int) -> bytes | None:
    """Скачивает самую маленькую аватарку пользователя из Telegram."""
    try:
        photos = await bot.get_user_profile_photos(user_id, limit=1)
        if photos.total_count > 0:
            # photos[0][0] - самое маленькое разрешение, скачивается мгновенно
            file_id = photos.photos[0][0].file_id 
            file = await bot.get_file(file_id)
            io_stream = io.BytesIO()
            await bot.download_file(file.file_path, io_stream)
            return io_stream.getvalue()
    except Exception as e:
        print(f"Ошибка загрузки аватара для {user_id}: {e}")
    return None

@router.callback_query(F.data == "menu:stats")
async def show_stats(callback: CallbackQuery):
    user_id = callback.from_user.id
    stats = await get_user_stats(user_id)

    if not stats: return await callback.answer("Сначала начни учиться!")

    level_info = get_level_info(stats['xp'])
    
    stats_image = await asyncio.to_thread(
        create_stats_card,
        xp=stats['xp'], level=level_info['level'],
        streak=stats['current_streak'], best_streak=stats['best_streak'],
        cards_learned=stats['total_learned'], total_possible=(46 + 46 + 22),
        progress=stats.get("cards_by_type", {})
    )

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏆 Достижения", callback_data="menu:achievements")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="menu:back")],
    ])

    try: await callback.message.delete()
    except: pass
    await callback.message.answer_photo(photo=BufferedInputFile(stats_image, filename="stats.png"), reply_markup=kb)
    await callback.answer()


@router.callback_query(F.data.startswith("menu:top"))
async def show_leaderboard(callback: CallbackQuery):
    """Отображает топ игроков с аватарками."""
    parts = callback.data.split(":")
    mode = parts[2] if len(parts) > 2 else "xp"
    
    if mode == "blitz":
        players = await get_top_blitz(10)
        title = "РЕЙТИНГ (БЛИЦ)"
        score_key = "best_blitz_score"
    else:
        players = await get_top_players(10)
        title = "РЕЙТИНГ (ОПЫТ)"
        score_key = "xp"
        
    if not players: return await callback.answer("Рейтинг пока пуст!", show_alert=True)
    
    # Показываем часики, так как скачивание 10 аватарок займет пару секунд
    await callback.bot.send_chat_action(chat_id=callback.message.chat.id, action="upload_photo")
    
    # ПАРАЛЛЕЛЬНО скачиваем аватарки для всех топ-10 игроков
    async def get_player_with_avatar(p):
        av_bytes = await fetch_avatar(callback.bot, p['user_id'])
        return {**p, 'avatar_bytes': av_bytes}
    
    players_with_avatars = await asyncio.gather(*[get_player_with_avatar(p) for p in players])

    lb_image = await asyncio.to_thread(
        create_leaderboard_card,
        players=players_with_avatars,
        current_user_id=callback.from_user.id,
        title=title,
        score_key=score_key
    )

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="⭐ По Опыту" if mode == "blitz" else "➡️ ⭐ По Опыту", callback_data="menu:top:xp"),
            InlineKeyboardButton(text="⚡ По Блицу" if mode == "xp" else "➡️ ⚡ По Блицу", callback_data="menu:top:blitz")
        ],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="menu:back")]
    ])

    try: await callback.message.delete()
    except: pass
    await callback.message.answer_photo(photo=BufferedInputFile(lb_image, filename="leaderboard.png"), reply_markup=kb)
    await callback.answer()
