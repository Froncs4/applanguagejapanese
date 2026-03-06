"""
Клавиатуры главного меню.
"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo


def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    """Главное inline-меню."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🔤 Азбука", callback_data="menu:alphabet"),
            InlineKeyboardButton(text="🎓 JLPT", callback_data="menu:jlpt"),
        ],
        [
            InlineKeyboardButton(text="🧠 Практика", callback_data="menu:learn"),
            InlineKeyboardButton(text="📖 Повторение", callback_data="menu:review"),
        ],
        [
            InlineKeyboardButton(text="🗣️ ИИ-Сенсей", callback_data="menu:tutor"),
        ],
        [
            InlineKeyboardButton(text="📊 Статистика", callback_data="menu:stats"),
            InlineKeyboardButton(text="🏆 Рейтинг", callback_data="menu:top:xp"),
        ],
        [
            InlineKeyboardButton(text="❓ Помощь", callback_data="menu:help"),
        ],
    ])


def get_alphabet_keyboard(webapp_url: str) -> InlineKeyboardMarkup:
    """Меню азбуки - только интерактивная версия."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🌐 Открыть интерактивную азбуку", web_app=WebAppInfo(url=webapp_url))],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="menu:back")],
    ])


def get_jlpt_keyboard() -> InlineKeyboardMarkup:
    """Меню JLPT уровней."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📚 N5 — Начальный", callback_data="jlpt_level:n5")],
        [
            InlineKeyboardButton(text="🈁 Кандзи N5", callback_data="study_groups:kanji_n5"),
            InlineKeyboardButton(text="📝 Слова N5", callback_data="study_groups:words_n5"),
        ],
        [InlineKeyboardButton(text="✏️ Тест N5 (Микс)", callback_data="mode:learn:n5_mixed")],
        [InlineKeyboardButton(text="─────────────────", callback_data="noop")],
        [InlineKeyboardButton(text="📚 N4 — Продолжающий", callback_data="jlpt_level:n4")],
        [
            InlineKeyboardButton(text="🈁 Кандзи N4", callback_data="study_groups:kanji_n4"),
            InlineKeyboardButton(text="📝 Слова N4", callback_data="study_groups:words_n4"),
        ],
        [InlineKeyboardButton(text="✏️ Тест N4 (Микс)", callback_data="mode:learn:n4_mixed")],
        [InlineKeyboardButton(text="─────────────────", callback_data="noop")],
        [
            InlineKeyboardButton(text="⚡ Блиц 60 сек", callback_data="start_blitz"),
            InlineKeyboardButton(text="🎯 Адаптивный", callback_data="mode:learn:mixed"),
        ],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="menu:back")],
    ])


def get_reply_keyboard() -> ReplyKeyboardMarkup:
    """Reply-клавиатура для быстрого доступа."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📋 Меню"), KeyboardButton(text="📊 Статистика")],
            [KeyboardButton(text="🔤 Азбука"), KeyboardButton(text="🎓 JLPT")],
            [KeyboardButton(text="🧠 Практика"), KeyboardButton(text="🗣️ ИИ-Сенсей")],
        ],
        resize_keyboard=True
    )


def get_tutor_exit_keyboard() -> InlineKeyboardMarkup:
    """Кнопка выхода из чата с ИИ."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚪 Выйти из чата", callback_data="menu:back")]
    ])


def get_alpha_tests_keyboard(mode: str = "hiragana") -> InlineKeyboardMarkup:
    """Выбор тестов по группам азбуки."""
    groups = ["vowels", "k", "s", "t", "n", "h", "m", "y", "r", "w"]
    
    buttons = []
    
    # Переключатель Хирагана/Катакана
    if mode == "hiragana":
        buttons.append([
            InlineKeyboardButton(text="✅ Хирагана", callback_data="alpha_tests_hiragana"),
            InlineKeyboardButton(text="⬜ Катакана", callback_data="alpha_tests_katakana"),
        ])
    else:
        buttons.append([
            InlineKeyboardButton(text="⬜ Хирагана", callback_data="alpha_tests_hiragana"),
            InlineKeyboardButton(text="✅ Катакана", callback_data="alpha_tests_katakana"),
        ])
    
    # Кнопки групп (по 5 в ряд)
    for i in range(0, len(groups), 5):
        row = []
        for g in groups[i:i+5]:
            row.append(InlineKeyboardButton(
                text=g.upper(), 
                callback_data=f"start_alpha_test_{mode}_{g}"
            ))
        buttons.append(row)
    
    buttons.append([InlineKeyboardButton(text="⬅️ Назад", callback_data="menu:alphabet")])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)