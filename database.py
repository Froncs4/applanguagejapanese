"""
База данных с ежедневными целями, статистикой, блиц-рекордами,
настройками фонов и колонками для НОВЫХ АЧИВОК.
"""

import aiosqlite
from datetime import datetime, date
from config import DB_PATH

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT DEFAULT '',
                xp INTEGER DEFAULT 0,
                current_streak INTEGER DEFAULT 0,
                best_streak INTEGER DEFAULT 0,
                last_activity TEXT DEFAULT '',
                daily_goal INTEGER DEFAULT 10,
                daily_progress INTEGER DEFAULT 0,
                daily_date TEXT DEFAULT '',
                total_reviews INTEGER DEFAULT 0,
                correct_reviews INTEGER DEFAULT 0,
                created_at TEXT DEFAULT '',
                best_blitz_score INTEGER DEFAULT 0,
                weekly_progress INTEGER DEFAULT 0,
                weekly_date TEXT DEFAULT '',
                voice_msgs INTEGER DEFAULT 0,
                night_owl INTEGER DEFAULT 0,
                grammar_perfect INTEGER DEFAULT 0,
                wheel_date TEXT DEFAULT '',
                -- НОВЫЕ КОЛОНКИ ДЛЯ ЗАЩИТЫ ОТ НАКРУТКИ
                last_quiz_time TEXT DEFAULT '',
                daily_quiz_count INTEGER DEFAULT 0,
                last_quiz_date TEXT DEFAULT ''
            )
        """)
        
        # Безопасное добавление колонок, если их ещё нет
        new_columns = [
            "last_quiz_time TEXT DEFAULT ''",
            "daily_quiz_count INTEGER DEFAULT 0",
            "last_quiz_date TEXT DEFAULT ''"
        ]
        for col in new_columns:
            try:
                await db.execute(f"ALTER TABLE users ADD COLUMN {col}")
            except Exception:
                pass

        await db.execute("""
            CREATE TABLE IF NOT EXISTS card_progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                card_type TEXT NOT NULL,
                card_key TEXT NOT NULL,
                ease_factor REAL DEFAULT 2.5,
                interval_days REAL DEFAULT 0,
                repetitions INTEGER DEFAULT 0,
                next_review TEXT DEFAULT '',
                last_review TEXT DEFAULT '',
                UNIQUE(user_id, card_type, card_key)
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS media_cache (
                media_key TEXT PRIMARY KEY,
                file_id TEXT NOT NULL,
                media_type TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                setting_key TEXT PRIMARY KEY,
                setting_value TEXT NOT NULL
            )
        """)
        await db.commit()


# ==========================================================
# 1. ФОНЫ И КЭШИРОВАНИЕ
# ==========================================================
async def get_all_backgrounds() -> dict:
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT setting_key, setting_value FROM settings WHERE setting_key LIKE 'bg_%'")
        rows = await cursor.fetchall()
        return {row[0].replace('bg_', ''): row[1] for row in rows}

async def set_background(screen: str, bg_name: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT OR REPLACE INTO settings (setting_key, setting_value) VALUES (?, ?)", 
            (f"bg_{screen}", bg_name)
        )
        await db.commit()

async def get_cached_media(media_key: str) -> str | None:
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT file_id FROM media_cache WHERE media_key = ?", (media_key,))
        row = await cursor.fetchone()
        return row[0] if row else None

async def set_cached_media(media_key: str, file_id: str, media_type: str):
    now = datetime.now().isoformat()
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT OR REPLACE INTO media_cache (media_key, file_id, media_type, created_at) VALUES (?, ?, ?, ?)",
            (media_key, file_id, media_type, now)
        )
        await db.commit()


# ==========================================================
# 2. ПОЛЬЗОВАТЕЛИ И ПРОГРЕСС
# ==========================================================
async def get_or_create_user(user_id: int, username: str = "") -> dict:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        row = await cursor.fetchone()

        today = date.today().isoformat()
        now = datetime.now().isoformat()
        current_week = datetime.now().strftime("%Y-%W") # Текущий год и номер недели

        if row:
            user = dict(row)
            
            # Автолечение имени
            if username and (not user.get("username") or user.get("username") == "Ученик"):
                await db.execute("UPDATE users SET username = ? WHERE user_id = ?", (username, user_id))
                user["username"] = username

            # Сброс ежедневного прогресса
            if user.get("daily_date") != today:
                await db.execute(
                    "UPDATE users SET daily_progress = 0, daily_date = ? WHERE user_id = ?",
                    (today, user_id)
                )
                user["daily_progress"] = 0
                user["daily_date"] = today
                
            # Сброс Еженедельного челленджа
            if user.get("weekly_date") != current_week:
                await db.execute(
                    "UPDATE users SET weekly_progress = 0, weekly_date = ? WHERE user_id = ?",
                    (current_week, user_id)
                )
                user["weekly_progress"] = 0
                user["weekly_date"] = current_week

            # Сброс ежедневного счётчика тестов
            if user.get("last_quiz_date") != today:
                await db.execute(
                    "UPDATE users SET daily_quiz_count = 0, last_quiz_date = ? WHERE user_id = ?",
                    (today, user_id)
                )
                user["daily_quiz_count"] = 0
                user["last_quiz_date"] = today
                
            await db.commit()
            return user

        # Создание нового пользователя
        await db.execute(
            """INSERT INTO users (
                user_id, username, xp, current_streak, best_streak,
                last_activity, daily_goal, daily_progress, daily_date, total_reviews,
                correct_reviews, created_at, best_blitz_score, weekly_progress, weekly_date,
                last_quiz_time, daily_quiz_count, last_quiz_date
               ) VALUES (?, ?, 0, 0, 0, ?, 10, 0, ?, 0, 0, ?, 0, 0, ?, '', 0, ?)""",
            (user_id, username, now, today, now, current_week, today)
        )
        await db.commit()
        return await get_or_create_user(user_id, username)

async def update_stats_and_achievements(user_id: int, xp_amount: int = 0, is_grammar_perfect: bool = False, is_voice: bool = False, is_night: bool = False):
    """Единая функция обновления всех счетчиков для ачивок"""
    async with aiosqlite.connect(DB_PATH) as db:
        if xp_amount > 0: 
            await db.execute("UPDATE users SET xp = xp + ? WHERE user_id = ?", (xp_amount, user_id))
        if is_voice: 
            await db.execute("UPDATE users SET voice_msgs = voice_msgs + 1 WHERE user_id = ?", (user_id,))
        if is_night: 
            await db.execute("UPDATE users SET night_owl = 1 WHERE user_id = ?", (user_id,))
        if is_grammar_perfect: 
            await db.execute("UPDATE users SET grammar_perfect = grammar_perfect + 1 WHERE user_id = ?", (user_id,))
        await db.commit()

async def add_xp(user_id: int, amount: int) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE users SET xp = xp + ? WHERE user_id = ?", (amount, user_id))
        await db.commit()
        cursor = await db.execute("SELECT xp FROM users WHERE user_id = ?", (user_id,))
        row = await cursor.fetchone()
        return row[0] if row else 0

async def claim_wheel_reward(user_id: int, reward: int) -> bool:
    """Записывает результат рулетки. Возвращает False, если юзер уже крутил сегодня."""
    today = date.today().isoformat()
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT wheel_date FROM users WHERE user_id = ?", (user_id,))
        row = await cursor.fetchone()
        if not row: return False
        
        if row[0] == today:
            return False # Уже крутил сегодня!
            
        # Обновляем дату и начисляем опыт
        await db.execute("UPDATE users SET wheel_date = ?, xp = xp + ? WHERE user_id = ?", (today, reward, user_id))
        await db.commit()
        return True

async def add_daily_progress(user_id: int, amount: int = 1) -> tuple:
    """Обновляет и Ежедневный, и Еженедельный прогресс"""
    today = date.today().isoformat()
    current_week = datetime.now().strftime("%Y-%W")
    
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT daily_progress, daily_goal, daily_date, weekly_progress, weekly_date FROM users WHERE user_id = ?",
            (user_id,)
        )
        row = await cursor.fetchone()
        if not row: return 0, 10, False, False
        
        current_prog, goal, last_date, week_prog, week_date = row
        
        # Сброс ежедневного прогресса, если день сменился
        if last_date != today:
            current_prog = 0
            
        # Сброс недельного прогресса, если неделя сменилась
        if week_date != current_week:
            week_prog = 0
            
        new_prog = current_prog + amount
        new_week_prog = week_prog + amount
        
        just_completed_daily = (current_prog < goal and new_prog >= goal)
        just_completed_weekly = (week_prog < 50 and new_week_prog >= 50) # Цель недели: 50
        
        await db.execute(
            "UPDATE users SET daily_progress = ?, daily_date = ?, weekly_progress = ?, weekly_date = ? WHERE user_id = ?", 
            (new_prog, today, new_week_prog, current_week, user_id)
        )
        await db.commit()
        return new_prog, goal, just_completed_daily, just_completed_weekly

async def update_streak(user_id: int, correct: bool) -> dict:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT current_streak, best_streak, total_reviews, correct_reviews FROM users WHERE user_id = ?", (user_id,))
        row = await cursor.fetchone()
        if not row: return {"current_streak": 0, "best_streak": 0}

        current, best = row["current_streak"], row["best_streak"]
        total = row["total_reviews"] + 1
        correct_count = row["correct_reviews"] + (1 if correct else 0)

        if correct:
            current += 1
            if current > best: best = current
        else:
            current = 0

        today = date.today().isoformat()
        await db.execute(
            """UPDATE users SET current_streak = ?, best_streak = ?, last_activity = ?,
               total_reviews = ?, correct_reviews = ? WHERE user_id = ?""",
            (current, best, today, total, correct_count, user_id)
        )
        await db.commit()
        return {"current_streak": current, "best_streak": best}

async def update_blitz_score(user_id: int, score: int) -> bool:
    """Обновляет рекорд блица."""
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT best_blitz_score FROM users WHERE user_id = ?", (user_id,))
        row = await cursor.fetchone()
        if not row: return False
        
        current_best = row[0]
        if score > current_best:
            await db.execute("UPDATE users SET best_blitz_score = ? WHERE user_id = ?", (score, user_id))
            await db.commit()
            return True
        return False

async def get_weakest_cards(user_id: int, card_type: str, limit: int = 5) -> list:
    """Возвращает карточки, в которых юзер чаще всего ошибается (самый низкий ease_factor)"""
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT card_key FROM card_progress WHERE user_id = ? AND card_type = ? AND repetitions > 0 ORDER BY ease_factor ASC LIMIT ?", 
            (user_id, card_type, limit)
        )
        rows = await cursor.fetchall()
        return [row[0] for row in rows]

async def get_user_stats(user_id: int) -> dict:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        user = await cursor.fetchone()
        if not user: return {}

        cursor = await db.execute("SELECT card_type, COUNT(*) as count FROM card_progress WHERE user_id = ? AND repetitions > 0 GROUP BY card_type", (user_id,))
        progress = {row["card_type"]: row["count"] for row in await cursor.fetchall()}

        cursor = await db.execute("SELECT COUNT(*) FROM card_progress WHERE user_id = ? AND repetitions > 0", (user_id,))
        total_learned = (await cursor.fetchone())[0]

        user_dict = dict(user)
        user_dict['accuracy'] = user_dict.get("correct_reviews", 0) / max(user_dict.get("total_reviews", 1), 1)
        return {**user_dict, "cards_by_type": progress, "total_learned": total_learned}

async def get_card_progress(user_id: int, card_type: str, card_key: str) -> dict | None:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM card_progress WHERE user_id = ? AND card_type = ? AND card_key = ?", (user_id, card_type, card_key))
        row = await cursor.fetchone()
        return dict(row) if row else None

async def upsert_card_progress(user_id: int, card_type: str, card_key: str, ease_factor: float, interval_days: float, repetitions: int, next_review: str):
    now = datetime.now().isoformat()
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """INSERT INTO card_progress (user_id, card_type, card_key, ease_factor, interval_days, repetitions, next_review, last_review)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)
               ON CONFLICT(user_id, card_type, card_key) DO UPDATE SET
                   ease_factor = excluded.ease_factor, interval_days = excluded.interval_days,
                   repetitions = excluded.repetitions, next_review = excluded.next_review, last_review = ?""",
            (user_id, card_type, card_key, ease_factor, interval_days, repetitions, next_review, now, now)
        )
        await db.commit()

async def get_top_players(limit: int = 10) -> list[dict]:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT user_id, username, xp, current_streak FROM users ORDER BY xp DESC LIMIT ?", (limit,))
        return [dict(row) for row in await cursor.fetchall()]

async def get_top_blitz(limit: int = 10) -> list[dict]:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT user_id, username, xp, best_blitz_score, current_streak FROM users ORDER BY best_blitz_score DESC LIMIT ?", (limit,))
        return [dict(row) for row in await cursor.fetchall()]

async def get_users_for_reminders() -> list[int]:
    now = datetime.now().isoformat()
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT DISTINCT user_id FROM card_progress WHERE next_review <= ?", (now,))
        return [row[0] for row in await cursor.fetchall()]


# ==========================================================
# НОВЫЕ ФУНКЦИИ ДЛЯ КОНТРОЛЯ ТЕСТОВ
# ==========================================================
async def check_quiz_cooldown(user_id: int) -> tuple[bool, int]:
    """
    Проверяет, может ли пользователь проходить тест.
    Возвращает (разрешено_ли, сколько_осталось_секунд)
    """
    from config import QUIZ_COOLDOWN, MAX_DAILY_QUIZZES
    today = date.today().isoformat()
    now = datetime.now()
    
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT last_quiz_time, daily_quiz_count, last_quiz_date FROM users WHERE user_id = ?",
            (user_id,)
        )
        row = await cursor.fetchone()
        if not row:
            return True, 0
        
        last_time_str, daily_count, last_date = row
        
        # Если сменился день, сбрасываем счётчик (хотя это уже делается в get_or_create_user, но на всякий случай)
        if last_date != today:
            daily_count = 0
            last_time_str = None
        
        # Проверка дневного лимита
        if MAX_DAILY_QUIZZES > 0 and daily_count >= MAX_DAILY_QUIZZES:
            return False, 0
        
        # Проверка кулдауна
        if last_time_str:
            last_time = datetime.fromisoformat(last_time_str)
            delta = now - last_time
            if delta.total_seconds() < QUIZ_COOLDOWN:
                remaining = QUIZ_COOLDOWN - int(delta.total_seconds())
                return False, remaining
        
        return True, 0


async def update_quiz_attempt(user_id: int):
    """Обновляет время последнего теста и счётчик"""
    today = date.today().isoformat()
    now = datetime.now().isoformat()
    
    async with aiosqlite.connect(DB_PATH) as db:
        # Сначала проверяем, не сменился ли день
        cursor = await db.execute("SELECT last_quiz_date, daily_quiz_count FROM users WHERE user_id = ?", (user_id,))
        row = await cursor.fetchone()
        if row:
            last_date, count = row
            if last_date != today:
                count = 0
        else:
            count = 0
            
        await db.execute(
            """UPDATE users SET last_quiz_time = ?, daily_quiz_count = ?, last_quiz_date = ?
               WHERE user_id = ?""",
            (now, count + 1, today, user_id)
        )
        await db.commit()