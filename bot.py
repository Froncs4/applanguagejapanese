"""
Точка входа: бот + API сервер.
"""

import asyncio
import logging
from aiohttp import web

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from database import init_db, get_all_backgrounds
import images
from handlers import get_all_routers
from scheduler import setup_scheduler
from middleware import AntiSpamMiddleware
from api import create_api_app

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)


async def main():
    logger.info("Инициализация базы данных...")
    await init_db()
    
    # Восстанавливаем фоны
    saved_bgs = await get_all_backgrounds()
    for screen, bg in saved_bgs.items():
        if screen in images.SCREEN_BACKGROUNDS and bg in images.ASSETS_URLS:
            images.SCREEN_BACKGROUNDS[screen] = bg
    
    # Создаём бота
    bot = Bot(
        token=BOT_TOKEN, 
        default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)
    )
    dp = Dispatcher(storage=MemoryStorage())
    
    # Middleware
    dp.callback_query.middleware(AntiSpamMiddleware(limit_seconds=0.7))
    
    # Роутеры
    for router in get_all_routers():
        dp.include_router(router)
    logger.info(f"Подключено роутеров: {len(get_all_routers())}")
    
    # Планировщик
    scheduler = setup_scheduler(bot)
    scheduler.start()
    
    # API сервер
    api_app = create_api_app()
    api_runner = web.AppRunner(api_app)
    await api_runner.setup()
    api_site = web.TCPSite(api_runner, '0.0.0.0', 8080)
    await api_site.start()
    logger.info("API сервер запущен на порту 8080")
    
    # Запуск бота
    logger.info("Бот запускается...")
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await api_runner.cleanup()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())