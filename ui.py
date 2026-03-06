"""
UI компоненты — красивое оформление.
"""

# ============================================================
# ЭМОДЗИ И СИМВОЛЫ
# ============================================================

# Прогресс-бары
BAR_FULL = "▓"
BAR_EMPTY = "░"
BAR_START = "┃"
BAR_END = "┃"

# Рамки для карточек
CARD_TOP = "╭─────────────────────────╮"
CARD_MID = "│"
CARD_BOT = "╰─────────────────────────╯"

# Декоративные элементы
SPARKLES = "✨"
STAR = "⭐"
FIRE = "🔥"
CHECK = "✅"
CROSS = "❌"
TROPHY = "🏆"
MEDAL = "🎖️"
BOOK = "📚"
BRAIN = "🧠"
TARGET = "🎯"
ROCKET = "🚀"
LIGHTNING = "⚡"
HEART = "❤️"
DIAMOND = "💎"
CROWN = "👑"

# Уровни
LEVEL_ICONS = {
    1: "🥚", 2: "🐣", 3: "🐥", 4: "🐤", 5: "🐔",
    6: "🦅", 7: "🔥", 8: "⭐", 9: "💫", 10: "👑",
    11: "💎", 12: "🌟", 13: "🎯", 14: "🏆", 15: "🐉",
}

# Streak визуализация
STREAK_MILESTONES = {
    0: "💨", 5: "🔥", 10: "🔥🔥", 15: "🔥🔥🔥",
    25: "💥", 50: "⚡", 100: "👑"
}


# ============================================================
# ФУНКЦИИ ГЕНЕРАЦИИ UI
# ============================================================

def progress_bar(current: int, total: int, length: int = 10) -> str:
    """Генерирует красивый прогресс-бар."""
    if total == 0:
        filled = 0
    else:
        filled = int(current / total * length)
    
    bar = BAR_FULL * filled + BAR_EMPTY * (length - filled)
    percent = int(current / total * 100) if total > 0 else 0
    return f"{BAR_START}{bar}{BAR_END} {percent}%"


def get_level_info(xp: int) -> dict:
    """
    Вычисляет уровень и прогресс.
    Формула: каждый уровень требует level * 100 XP.
    """
    level = 1
    xp_remaining = xp
    total_for_level = 100
    
    while xp_remaining >= total_for_level:
        xp_remaining -= total_for_level
        level += 1
        total_for_level = level * 100
    
    icon = LEVEL_ICONS.get(level, LEVEL_ICONS.get(min(level, 15), "🐉"))
    
    return {
        "level": level,
        "icon": icon,
        "current_xp": xp_remaining,
        "needed_xp": total_for_level,
        "total_xp": xp,
        "progress_bar": progress_bar(xp_remaining, total_for_level, 10)
    }


def get_streak_display(streak: int) -> str:
    """Красивое отображение streak."""
    icon = "💨"
    for threshold, emoji in sorted(STREAK_MILESTONES.items(), reverse=True):
        if streak >= threshold:
            icon = emoji
            break
    
    if streak == 0:
        return f"{icon} Нет серии"
    elif streak < 5:
        return f"{icon} {streak} подряд"
    else:
        return f"{icon} {streak} подряд — Отлично!"


def create_card_display(symbol: str, card_type: str) -> str:
    """Создаёт красивую карточку для символа."""
    
    # Определяем ширину карточки
    padding = 10
    
    # Заголовок по типу
    headers = {
        "hiragana": "🅰️ ХИРАГАНА",
        "katakana": "🅱️ КАТАКАНА", 
        "kanji": "🈁 КАНДЗИ",
        "words": "📝 СЛОВО"
    }
    header = headers.get(card_type, "📚 КАРТОЧКА")
    
    card = f"""
┏━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃      {header}          ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃                         ┃
┃         {symbol:^5}          ┃
┃                         ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━┛
"""
    return card.strip()


def create_result_card(correct: bool, symbol: str, answer: str, 
                       xp_gained: int = 0, total_xp: int = 0, 
                       streak: int = 0, best_streak: int = 0) -> str:
    """Создаёт красивую карточку результата."""
    
    if correct:
        header = f"{CHECK} ПРАВИЛЬНО! {SPARKLES}"
        color_line = "🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢"
    else:
        header = f"{CROSS} НЕПРАВИЛЬНО"
        color_line = "🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴"
    
    streak_display = get_streak_display(streak)
    
    if correct:
        result = f"""
{color_line}

{header}

┌─────────────────────────┐
│  {symbol}  →  {answer:<15} │
└─────────────────────────┘

   {STAR} +{xp_gained} XP (всего: {total_xp})
   {streak_display}

{color_line}
"""
    else:
        result = f"""
{color_line}

{header}

┌─────────────────────────┐
│  {symbol}  →  {answer:<15} │
└─────────────────────────┘

   {BRAIN} Запомни этот ответ!
   🔄 Карточка скоро повторится

{color_line}
"""
    
    return result.strip()


def create_welcome_message(name: str, level_info: dict, streak: int) -> str:
    """Создаёт приветственное сообщение."""
    
    streak_display = get_streak_display(streak)
    
    return f"""
🎌 ━━━━━━━━━━━━━━━━━━━━━━ 🎌

   Привет, **{name}**!
   
   Добро пожаловать в
   **Japanese Learning Bot**

🎌 ━━━━━━━━━━━━━━━━━━━━━━ 🎌

{level_info['icon']} Уровень **{level_info['level']}**
{level_info['progress_bar']}
{STAR} XP: {level_info['total_xp']}

{streak_display}

━━━━━━━━━━━━━━━━━━━━━━━━━━

📚 **Обучение:**
🅰️ Хирагана и Катакана
🈁 Кандзи (N5, N4)
📝 Лексика (N5, N4)

⚡ **Спец-режимы:**
� Аудио-викторина
⏱ Блиц (60 секунд)

━━━━━━━━━━━━━━━━━━━━━━━━━━

⬇️ Выбери действие:
"""


def create_stats_message(stats: dict, cards_progress: dict) -> str:
    """Создаёт красивое сообщение статистики."""
    
    level_info = get_level_info(stats['xp'])
    streak_display = get_streak_display(stats['current_streak'])
    
    # Прогресс по разделам
    sections = ""
    section_data = [
        ("🅰️ Хирагана", "hiragana", 46),
        ("🅱️ Катакана", "katakana", 46),
        ("🈁 Кандзи", "kanji", 22),
        ("📝 Слова", "words", 13),
    ]
    
    for name, key, total in section_data:
        learned = cards_progress.get(key, 0)
        bar = progress_bar(learned, total, 8)
        sections += f"\n{name}\n{bar} ({learned}/{total})\n"
    
    return f"""
📊 ━━━ ТВОЯ СТАТИСТИКА ━━━ 📊

{level_info['icon']} **Уровень {level_info['level']}**
{level_info['progress_bar']}
До следующего: {level_info['needed_xp'] - level_info['current_xp']} XP

━━━━━━━━━━━━━━━━━━━━━━━━━━

{STAR} **Всего XP:** {stats['xp']}
{FIRE} **Текущая серия:** {stats['current_streak']}
{TROPHY} **Лучшая серия:** {stats['best_streak']}
{BOOK} **Изучено карточек:** {stats['total_learned']}

━━━━━━━━━━━━━━━━━━━━━━━━━━

📈 **ПРОГРЕСС ПО РАЗДЕЛАМ:**
{sections}
━━━━━━━━━━━━━━━━━━━━━━━━━━

{streak_display}
"""


def create_quiz_message(card_type: str, symbol: str, hint: str = None, context: str = None) -> str:
    """Создаёт сообщение для квиза."""
    
    questions = {
        "hiragana": "Как читается этот символ?",
        "katakana": "Как читается этот символ?",
        "kanji": "Что означает этот иероглиф?",
        "words": "Как переводится это слово?",
        "audio_quiz": "Какой символ вы услышали?"
    }
    
    question = questions.get(card_type, "Выбери правильный ответ:")
    
    message = f"""
❓ **{question}**

⬇️ Выбери ответ:
"""
    
    if context:
        message = message.replace("❓", f"📝 **Контекст:** {context}\n\n❓")

    if hint:
        message += f"\n💡 Подсказка: {hint}"
    
    return message


def create_mode_select_message(action: str) -> str:
    """Сообщение выбора режима."""
    
    if action == "learn":
        header = f"{BOOK} РЕЖИМ ИЗУЧЕНИЯ"
        desc = "Случайные карточки для практики"
    else:
        header = f"{BRAIN} РЕЖИМ ПОВТОРЕНИЯ"
        desc = "Карточки по системе SRS"
    
    return f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━

{header}

{desc}

━━━━━━━━━━━━━━━━━━━━━━━━━━

📚 Выбери раздел:
"""


def create_achievement_message(achievement: str) -> str:
    """Сообщение о достижении."""
    
    return f"""
🎊 ━━━━━━━━━━━━━━━━━━━━ 🎊

{TROPHY} **ДОСТИЖЕНИЕ!**

{achievement}

🎊 ━━━━━━━━━━━━━━━━━━━━ 🎊
"""


def create_streak_bonus_message(streak: int, bonus_xp: int) -> str:
    """Сообщение о бонусе за серию."""
    
    fires = "🔥" * min(streak // 5, 10)
    
    return f"""
{fires}

⚡ **БОНУС ЗА СЕРИЮ!**

{streak} правильных подряд!
+{bonus_xp} бонусных XP

{fires}
"""