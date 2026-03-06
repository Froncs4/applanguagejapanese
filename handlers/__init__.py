"""
Регистрация всех роутеров.
"""

from aiogram import Router
from handlers.start import router as start_router
from handlers.study import router as study_router
from handlers.stats import router as stats_router
from handlers.dictionary import router as dict_router
from handlers.tutor import router as tutor_router

# Заменили quiz2 обратно на quiz
from handlers.quiz import router as quiz_router


def get_all_routers() -> list[Router]:
    """Возвращает список всех роутеров."""
    return [
        start_router, 
        study_router, 
        quiz_router, 
        stats_router, 
        dict_router, 
        tutor_router
    ]
