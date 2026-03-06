"""
Защита от спама кликами по inline-кнопкам.
"""
import time
from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, CallbackQuery

class AntiSpamMiddleware(BaseMiddleware):
    def __init__(self, limit_seconds: float = 0.7):
        self.limit = limit_seconds
        self.users_last_click = {}

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        # Проверяем только нажатия на инлайн-кнопки
        if isinstance(event, CallbackQuery):
            user_id = event.from_user.id
            now = time.time()
            last_click = self.users_last_click.get(user_id, 0)
            
            # Если прошло меньше limit_seconds, игнорируем клик
            if now - last_click < self.limit:
                try:
                    await event.answer("⏳ Не так быстро!", show_alert=False)
                except:
                    pass
                return  # Прерываем обработку
                
            self.users_last_click[user_id] = now
            
        return await handler(event, data)
