"""
Клавиатуры для викторины.
"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.state import StatesGroup, State

class QuizStates(StatesGroup):
    typing_answer = State()
    blitz_mode = State()

def get_quiz_keyboard(
    options: list[str],
    correct_index: int,
    card_type: str,
    card_key: str
) -> InlineKeyboardMarkup:
    """Клавиатура с вариантами ответа."""
    letters = ["А", "Б", "В", "Г"]
    
    buttons = []
    for i, option in enumerate(options):
        letter = letters[i] if i < len(letters) else str(i + 1)
        callback = f"answer:{card_type}:{card_key}:{i}:{correct_index}"
        buttons.append([
            InlineKeyboardButton(text=f"{letter}. {option}", callback_data=callback)
        ])
    
    buttons.append([
        InlineKeyboardButton(text="⌨️ Ввести ответ", callback_data=f"type_answer:{card_type}:{card_key}:{correct_index}"),
    ])
    
    buttons.append([
        InlineKeyboardButton(text="💡 Подсказка", callback_data=f"hint:{card_type}:{card_key}"),
        InlineKeyboardButton(text="⏭ Пропустить", callback_data=f"skip:{card_type}"),
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_result_keyboard(
    card_type: str, 
    action: str = "learn", 
    correct: bool = True,
    group_key: str = None
) -> InlineKeyboardMarkup:
    """Кнопки после ответа."""
    if correct:
        next_text = "➡️ Дальше"
    else:
        next_text = "🔄 Ещё раз"
    
    # Формируем callback с учётом группы
    if group_key:
        next_callback = f"next:{action}:{card_type}:{group_key}"
        back_callback = f"study_groups:{card_type}"
        back_text = "📚 К группам"
    else:
        next_callback = f"next:{action}:{card_type}:"
        back_callback = "menu:back"
        back_text = "🏠 Меню"
    
    buttons = [
        [
            InlineKeyboardButton(text=next_text, callback_data=next_callback),
        ],
        [
            InlineKeyboardButton(text="📊 Прогресс", callback_data="menu:stats"),
            InlineKeyboardButton(text=back_text, callback_data=back_callback),
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)