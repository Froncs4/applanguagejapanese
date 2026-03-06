"""
Упрощённая система интервальных повторений (SM-2).
"""
from datetime import datetime, timedelta
from database import get_card_progress, upsert_card_progress

MIN_EASE = 1.3
MAX_EASE = 2.5
DEFAULT_EASE = 2.5
MAX_INTERVAL_DAYS = 365 * 3  # <-- ЗАЩИТА: Максимум 3 года!

def calculate_next_review(repetitions: int, ease_factor: float, interval_days: float, correct: bool) -> tuple:
    if correct:
        repetitions += 1
        if repetitions == 1: interval_days = 1.0
        elif repetitions == 2: interval_days = 3.0
        else: interval_days *= ease_factor
        ease_factor = min(ease_factor + 0.1, MAX_EASE)
    else:
        repetitions = 0
        interval_days = 0.0028
        ease_factor = max(ease_factor - 0.2, MIN_EASE)

    # Применяем защиту от переполнения даты
    interval_days = min(interval_days, MAX_INTERVAL_DAYS)
    
    next_review = datetime.now() + timedelta(days=interval_days)
    return repetitions, ease_factor, interval_days, next_review.isoformat()

async def process_answer(user_id: int, card_type: str, card_key: str, correct: bool) -> dict:
    progress = await get_card_progress(user_id, card_type, card_key)
    if progress:
        reps, ease, interval = progress["repetitions"], progress["ease_factor"], progress["interval_days"]
    else:
        reps, ease, interval = 0, DEFAULT_EASE, 0.0

    new_reps, new_ease, new_interval, next_review = calculate_next_review(reps, ease, interval, correct)

    await upsert_card_progress(user_id, card_type, card_key, new_ease, new_interval, new_reps, next_review)

    return {"repetitions": new_reps, "ease_factor": new_ease, "interval_days": new_interval, "next_review": next_review}