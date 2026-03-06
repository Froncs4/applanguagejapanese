"""
Конфигурация бота.
"""

import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Токен из переменных окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Путь к базе данных
DB_PATH = os.getenv("DB_PATH", "japanese_bot.db")

# XP настройки
XP_CORRECT = 10
XP_STREAK_BONUS = 5
STREAK_BONUS_EVERY = 5

# Количество вариантов ответа
QUIZ_OPTIONS_COUNT = 4

# === НОВЫЕ НАСТРОЙКИ ===
# ID администраторов, которым разрешена команда /setbg (через запятую в .env)
ADMIN_IDS = [int(id.strip()) for id in os.getenv("ADMIN_IDS", "").split(",") if id.strip()]

# Кулдаун для тестов в секундах (например, 3600 = 1 час)
QUIZ_COOLDOWN = int(os.getenv("QUIZ_COOLDOWN", 3600))

# Максимальное количество прохождений теста в день (0 - без ограничений)
MAX_DAILY_QUIZZES = int(os.getenv("MAX_DAILY_QUIZZES", 5))

# Размер очереди штрафных карточек
PENALTY_QUEUE_SIZE = 10

# Таймаут для HTTP-запросов (секунды)
HTTP_TIMEOUT = int(os.getenv("HTTP_TIMEOUT", 10))