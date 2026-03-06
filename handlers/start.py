"""
Обработчики: /start, главное меню, достижения и Web App Игры.
"""

import io
import asyncio
import urllib.parse
import random
import hmac
import hashlib
import json

from aiogram import Router, F
from aiogram.enums import ContentType
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import BufferedInputFile, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from database import (
    get_or_create_user, get_user_stats, set_background, add_xp,
    add_daily_progress, check_quiz_cooldown, update_quiz_attempt
)
from keyboards.menu import (
    get_main_menu_keyboard, get_alphabet_keyboard, get_jlpt_keyboard,
    get_reply_keyboard, get_alpha_tests_keyboard, get_tutor_exit_keyboard
)
from ui import get_level_info
import images
from images import create_welcome_banner, create_mode_select_card, create_achievements_card, create_alphabet_card
from config import BOT_TOKEN, ADMIN_IDS

router = Router()

# ==========================================================
# ФУНКЦИЯ ПРОВЕРКИ ПОДПИСИ WEB APP DATA
# ==========================================================
def verify_telegram_auth(init_data: str) -> dict | None:
    """
    Проверяет подпись initData от Telegram WebApp.
    Возвращает данные пользователя или None если невалидно.
    """
    try:
        parsed = dict(urllib.parse.parse_qsl(init_data))
        
        check_hash = parsed.pop('hash', None)
        if not check_hash:
            return None
        
        # Сортируем и формируем строку
        data_check_string = '\n'.join(
            f"{k}={v}" for k, v in sorted(parsed.items())
        )
        
        # Создаём секретный ключ
        secret_key = hmac.new(
            b"WebAppData", 
            BOT_TOKEN.encode(), 
            hashlib.sha256
        ).digest()
        
        # Проверяем хэш
        calculated_hash = hmac.new(
            secret_key,
            data_check_string.encode(),
            hashlib.sha256
        ).hexdigest()
        
        if calculated_hash != check_hash:
            return None
        
        # Парсим user
        user_data = json.loads(parsed.get('user', '{}'))
        return user_data
        
    except Exception as e:
        print(f"Auth error: {e}")
        return None

# ==========================================================
# 1. ГЕНЕРАТОРЫ ССЫЛОК ДЛЯ WEB APP
# ==========================================================
GITHUB_URL = "https://froncs4.github.io/applanguagejapanese/"

def generate_webapp_url() -> str: return f"{GITHUB_URL}?mode=quiz&v={random.randint(10000, 99999)}"
def generate_swipe_url() -> str: return f"{GITHUB_URL}?mode=swipe&v={random.randint(10000, 99999)}"
def generate_grammar_url() -> str: return f"{GITHUB_URL}?mode=grammar&v={random.randint(10000, 99999)}"
def generate_wheel_url() -> str: 
    return f"https://froncs4.github.io/applanguagejapanese/wheel.html?v={random.randint(10000, 99999)}"
def generate_alphabet_url() -> str: return f"{GITHUB_URL}?mode=alphabet&v={random.randint(10000, 99999)}"

def generate_alpha_test_url(azbuka: str, group: str) -> str:
    return f"{GITHUB_URL}?mode=alphatest&azbuka={azbuka}&group={group}&v={random.randint(10000, 99999)}"


@router.message(F.content_type == ContentType.WEB_APP_DATA)
async def web_app_data_handler(message: Message):
    """
    Обрабатывает данные, присланные из Web App.
    Ожидается, что Web App отправляет JSON с полями:
        type: "quiz_result", "swipe_result", "grammar_result", "alphatest_result", "wheel_reward"
        score: число (если применимо)
        initData: строка с исходными данными от Telegram
    """
    data_str = message.web_app_data.data
    user_id = message.from_user.id

    try:
        # Пытаемся распарсить JSON
        data = json.loads(data_str)
    except json.JSONDecodeError:
        # Если не JSON, возможно старая версия (просто результат) - игнорируем для безопасности
        await message.answer("❌ Ошибка: неверный формат данных. Пожалуйста, обновите Web App.")
        return

    # Проверяем подпись, если есть initData
    init_data = data.get("initData")
    if init_data:
        auth_data = verify_telegram_auth(init_data)
        if not auth_data or auth_data.get("id") != user_id:
            await message.answer("❌ Ошибка аутентификации. Попробуйте снова.")
            return
    else:
        # Если нет initData, отклоняем запрос (старая версия)
        await message.answer("❌ Устаревшая версия Web App. Пожалуйста, обновите.")
        return

    # Определяем тип
    result_type = data.get("type")
    score = data.get("score", 0)

    # Проверка кулдауна для тестов (кроме рулетки)
    if result_type in ["quiz_result", "swipe_result", "grammar_result", "alphatest_result"]:
        allowed, remaining = await check_quiz_cooldown(user_id)
        if not allowed:
            if remaining > 0:
                minutes = remaining // 60
                seconds = remaining % 60
                await message.answer(f"⏳ Подождите {minutes} мин {seconds} сек перед следующим тестом.")
            else:
                await message.answer("❌ Вы исчерпали дневной лимит тестов.")
            return

        # Обновляем время последнего теста
        await update_quiz_attempt(user_id)

    # Обработка всех типов результатов
    if result_type in ["quiz_result", "swipe_result", "grammar_result", "alphatest_result"]:
        # 10 XP за каждый правильный ответ
        xp_gained = score * 10
        
        if xp_gained > 0:
            await add_xp(user_id, xp_gained)
            await add_daily_progress(user_id, score)  # Добавляем в дневной прогресс
        
        # Определяем режим для сообщения
        mode_names = {
            "quiz_result": "Web-Квизе",
            "swipe_result": "Свайп-карточках",
            "grammar_result": "Грамматике",
            "alphatest_result": "Тесте Азбуки"
        }
        mode_name = mode_names.get(result_type, "Web-Квизе")
        
        # Отправляем результат
        if score >= 5:
            await message.answer(
                f"🏆 **ОТЛИЧНО!** Ты ответил на {score} вопросов в {mode_name}!\n\n"
                f"Получено: **+{xp_gained} XP** ⭐️"
            )
        elif score > 0:
            await message.answer(
                f"👏 Хорошая работа в {mode_name}!\n"
                f"Правильных ответов: {score}\n\n"
                f"Получено: **+{xp_gained} XP** ⭐️"
            )
        else:
            await message.answer(
                f"📚 Нужно ещё потренироваться!\n"
                f"Результат: 0 правильных.\n\n"
                f"XP не начислен, но ты справишься в следующий раз!"
            )

    elif result_type == "wheel_reward":
        from database import claim_wheel_reward
        success = await claim_wheel_reward(user_id, score)
        if success:
            await message.answer(f"🎡 Вы выиграли **+{score} XP** в рулетке!")
        else:
            await message.answer("❌ Вы уже крутили рулетку сегодня.")


# ==========================================================
# 2. АВАТАР И ГЛАВНОЕ МЕНЮ
# ==========================================================
async def fetch_avatar(bot, user_id: int) -> bytes | None:
    try:
        photos = await bot.get_user_profile_photos(user_id, limit=1)
        if photos.total_count > 0:
            file_id = photos.photos[0][0].file_id 
            file = await bot.get_file(file_id)
            io_stream = io.BytesIO()
            await bot.download_file(file.file_path, io_stream)
            return io_stream.getvalue()
    except Exception:
        pass
    return None


@router.message(CommandStart())
@router.message(Command("menu"))
async def cmd_start_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.bot.send_chat_action(chat_id=message.chat.id, action="upload_photo")

    real_name = message.from_user.first_name or message.from_user.username or "Ученик"
    user = await get_or_create_user(message.from_user.id, real_name)
    level_info = get_level_info(user['xp'])
    av_bytes = await fetch_avatar(message.bot, message.from_user.id)

    banner = await asyncio.to_thread(
        create_welcome_banner, 
        username=real_name, 
        level=level_info['level'], 
        xp=user['xp'], 
        streak=user['current_streak'], 
        avatar_bytes=av_bytes
    )

    reply_kb = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🎮 Web-Квиз", web_app=WebAppInfo(url=generate_webapp_url())), 
                KeyboardButton(text="🎡 Рулетка", web_app=WebAppInfo(url=generate_wheel_url()))
            ],
            [
                KeyboardButton(text="📋 Меню"),
                KeyboardButton(text="📊 Статистика"),
            ]
        ],
        resize_keyboard=True
    )

    await message.answer_photo(
        photo=BufferedInputFile(banner, filename="menu.png"), 
        reply_markup=get_main_menu_keyboard()
    )
    
    await message.answer(
        "⬇️ Используй кнопки ниже для быстрого доступа:",
        reply_markup=reply_kb
    )


@router.callback_query(F.data == "menu:back")
async def menu_back(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    real_name = callback.from_user.first_name or callback.from_user.username or "Ученик"
    user = await get_or_create_user(callback.from_user.id, real_name)
    level_info = get_level_info(user['xp'])
    av_bytes = await fetch_avatar(callback.bot, callback.from_user.id)
    banner = await asyncio.to_thread(create_welcome_banner, username=real_name, level=level_info['level'], xp=user['xp'], streak=user['current_streak'], avatar_bytes=av_bytes)
    try: await callback.message.delete()
    except Exception: pass
    await callback.message.answer_photo(photo=BufferedInputFile(banner, filename="menu.png"), reply_markup=get_main_menu_keyboard())


# ==========================================================
# 3. НАСТРОЙКИ (ЗАЩИТА КОМАНДЫ /setbg)
# ==========================================================
@router.message(Command("setbg"))
async def cmd_setbg(message: Message):
    # Проверяем, является ли пользователь администратором
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("❌ У вас нет прав на выполнение этой команды.")
        return

    parts = message.text.split()
    if len(parts) != 3:
        return await message.answer(f"🛠 **Смена фонов**\n`/setbg [экран] [фон]`\nДоступные фоны: {', '.join(images.ASSETS_URLS.keys())}")
    if parts[1] in images.SCREEN_BACKGROUNDS and parts[2] in images.ASSETS_URLS:
        images.SCREEN_BACKGROUNDS[parts[1]] = parts[2]
        await set_background(parts[1], parts[2])
        await message.answer(f"✅ Фон для экрана **{parts[1]}** успешно изменён на `{parts[2]}`!")
    else:
        await message.answer("❌ Ошибка: Неверное имя экрана или фона.")


@router.message(Command("setname"))
async def cmd_setname(message: Message):
    parts = message.text.split(" ", 1)
    if len(parts) < 2: return await message.answer("📝 Напиши:\n`/setname ТвоёИмя`")
    new_name = images.clean_username(parts[1].strip())
    if not new_name or new_name == "Ученик": return await message.answer("❌ Имя должно содержать буквы.")
    import aiosqlite
    from config import DB_PATH
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE users SET username = ? WHERE user_id = ?", (new_name, message.from_user.id))
        await db.commit()
    await message.answer(f"✅ Имя изменено на **{new_name}**!")


# ==========================================================
# 4. НАВИГАЦИЯ ПО МЕНЮ (остаётся без изменений, но добавлены все обработчики)
# ==========================================================
@router.callback_query(F.data == "menu:alphabet")
async def menu_alphabet(callback: CallbackQuery):
    await callback.answer()
    
    # Используем функцию для азбуки
    image = await asyncio.to_thread(images.create_alphabet_card)
    
    try: 
        await callback.message.delete()
    except: 
        pass
    
    await callback.message.answer_photo(
        photo=BufferedInputFile(image, filename="alphabet.png"),
        reply_markup=get_alphabet_keyboard(generate_alphabet_url())
    )


@router.callback_query(F.data == "alpha_tests_select")
async def alpha_tests_select(callback: CallbackQuery):
    await callback.answer()
    try: await callback.message.edit_reply_markup(reply_markup=get_alpha_tests_keyboard("hiragana"))
    except: pass


@router.callback_query(F.data.startswith("alpha_tests_"))
async def alpha_tests_switch(callback: CallbackQuery):
    await callback.answer()
    mode = callback.data.split("_")[2]
    try: await callback.message.edit_reply_markup(reply_markup=get_alpha_tests_keyboard(mode))
    except: pass


@router.callback_query(F.data.startswith("start_alpha_test_"))
async def start_alpha_test(callback: CallbackQuery):
    await callback.answer()
    parts = callback.data.split("_")
    azbuka, group = parts[3], parts[4]
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎮 Начать тест", web_app=WebAppInfo(url=generate_alpha_test_url(azbuka, group)))],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="alpha_tests_select")]
    ])
    try: await callback.message.delete()
    except: pass
    image = await asyncio.to_thread(create_mode_select_card, "learn")
    await callback.message.answer_photo(photo=BufferedInputFile(image, filename="test.png"), caption=f"Тест по группе: {group.upper()}", reply_markup=kb)


@router.callback_query(F.data == "menu:jlpt")
async def menu_jlpt(callback: CallbackQuery):
    await callback.answer()
    image = await asyncio.to_thread(create_mode_select_card, "jlpt")
    try: await callback.message.delete()
    except Exception: pass
    await callback.message.answer_photo(photo=BufferedInputFile(image, filename="jlpt.png"), reply_markup=get_jlpt_keyboard())


@router.callback_query(F.data == "menu:learn")
async def menu_learn(callback: CallbackQuery):
    await callback.answer()
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🃏 Учить по карточкам (Tinder)", web_app=WebAppInfo(url=generate_swipe_url()))],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="menu:back")]
    ])
    image = await asyncio.to_thread(create_mode_select_card, "learn")
    try: await callback.message.delete()
    except Exception: pass
    await callback.message.answer_photo(photo=BufferedInputFile(image, filename="learn.png"), reply_markup=kb)


@router.callback_query(F.data == "menu:review")
async def menu_review(callback: CallbackQuery):
    await callback.answer()
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🧩 Интерактивная Грамматика", web_app=WebAppInfo(url=generate_grammar_url()))],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="menu:back")]
    ])
    image = await asyncio.to_thread(create_mode_select_card, "review")
    try: await callback.message.delete()
    except Exception: pass
    await callback.message.answer_photo(photo=BufferedInputFile(image, filename="review.png"), reply_markup=kb)


# === ЧАТ ИИ (Обычный текстово-голосовой режим внутри ТГ) ===
@router.callback_query(F.data == "menu:tutor")
async def menu_tutor_text(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    try: await callback.message.delete()
    except Exception: pass
    from handlers.tutor import start_tutor_chat
    await start_tutor_chat(callback, state)


@router.message(F.text == "🎲 Рулетка")
async def text_wheel(message: Message):
    wheel_url = generate_wheel_url()
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎲 Крутить рулетку!", web_app=WebAppInfo(url=wheel_url))],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="menu:back")]
    ])
    await message.answer("🎲 **Рулетка!**\n\nИспытай удачу и выиграй призовые XP!", reply_markup=kb)


@router.message(F.text == "🔤 Азбука")
async def text_alphabet(message: Message):
    alphabet_url = generate_alphabet_url()
    kb = get_alphabet_keyboard(alphabet_url)
    await message.answer("🔤 **Интерактивная Азбука!**\n\nИзучай хирагану и катакану в красивом Web App!", reply_markup=kb)


@router.message(F.text == "🗣️ ИИ-Сенсей")
async def text_tutor(message: Message):
    from handlers.tutor import start_tutor_chat
    from aiogram.fsm.context import FSMContext
    # Создаем фиктивный callback для совместимости
    class FakeCallback:
        def __init__(self, msg):
            self.message = msg
            self.from_user = msg.from_user
        async def answer(self):
            pass
    
    fake_callback = FakeCallback(message)
    from aiogram.fsm.context import FSMContext
    # Получаем FSM state из диспетчера
    state = FSMContext(storage=message.bot.dp.storage, chat_id=message.chat.id, user_id=message.from_user.id)
    await start_tutor_chat(fake_callback, state)


@router.message(F.text == "🎓 JLPT")
async def text_jlpt(message: Message):
    """Обработка текстовой кнопки JLPT."""
    image = await asyncio.to_thread(create_mode_select_card, "jlpt")
    await message.answer_photo(
        photo=BufferedInputFile(image, filename="jlpt.png"), 
        reply_markup=get_jlpt_keyboard()
    )


@router.message(F.text == "🧠 Практика")
async def text_practice(message: Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🃏 Учить по карточкам (Tinder)", web_app=WebAppInfo(url=generate_swipe_url()))],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="menu:back")]
    ])
    image = await asyncio.to_thread(create_mode_select_card, "learn")
    await message.answer_photo(
        photo=BufferedInputFile(image, filename="learn.png"), 
        reply_markup=kb
    )


@router.message(F.text == "📊 Статистика")
async def text_stats(message: Message):
    from database import get_user_stats
    from ui import get_level_info
    from images import create_stats_card
    
    user_id = message.from_user.id
    stats = await get_user_stats(user_id)

    if not stats: 
        return await message.answer("Сначала начни учиться!")

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

    await message.answer_photo(
        photo=BufferedInputFile(stats_image, filename="stats.png"), 
        reply_markup=kb
    )


@router.message(F.text == "📋 Меню")
async def text_menu(message: Message, state: FSMContext):
    # Просто вызываем существующую функцию главного меню
    await cmd_start_menu(message, state)


@router.callback_query(F.data == "menu:help")
async def menu_help(callback: CallbackQuery):
    await callback.answer()
    help_text = ("📖 КАК ПОЛЬЗОВАТЬСЯ\n\n1. АЗБУКА — учим символы Хираганы и Катаканы\n2. JLPT — учим иероглифы, слова и грамматику\n3. WEB-ИГРЫ — свайпы карточек, рулетка и тесты")
    kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="« Назад", callback_data="menu:back")]])
    try: await callback.message.delete()
    except Exception: pass
    await callback.message.answer(help_text, reply_markup=kb)


@router.callback_query(F.data == "menu:achievements")
async def menu_achievements(callback: CallbackQuery):
    await callback.answer()
    stats = await get_user_stats(callback.from_user.id)
    if not stats: return await callback.answer("Сначала начни учиться!", show_alert=True)
    img = await asyncio.to_thread(create_achievements_card, user_data=stats, page=0)
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Следующая страница ➡️", callback_data="achievements_page:1")],
        [InlineKeyboardButton(text="⬅️ В статистику", callback_data="menu:stats")]
    ])
    try: await callback.message.delete()
    except Exception: pass
    await callback.message.answer_photo(photo=BufferedInputFile(img, filename="ach.png"), reply_markup=kb)


@router.callback_query(F.data.startswith("achievements_page:"))
async def achievements_page(callback: CallbackQuery):
    await callback.answer()
    page = int(callback.data.split(":")[1])
    stats = await get_user_stats(callback.from_user.id)
    img = await asyncio.to_thread(create_achievements_card, user_data=stats, page=page)
    buttons = []
    if page > 0: buttons.append([InlineKeyboardButton(text="⬅️ Предыдущая страница", callback_data=f"achievements_page:{page-1}")])
    if page < 1: buttons.append([InlineKeyboardButton(text="Следующая страница ➡️", callback_data=f"achievements_page:{page+1}")])
    buttons.append([InlineKeyboardButton(text="⬅️ В статистику", callback_data="menu:stats")])
    try: await callback.message.delete()
    except Exception: pass
    await callback.message.answer_photo(photo=BufferedInputFile(img, filename="ach.png"), reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))