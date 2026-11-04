import os
import sys
import logging
import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

import database as db

from handlers.start import start_router
from handlers.daily_tip import daily_tip_router
from handlers.workout import workout_router
from handlers.nutrition import nutrition_router
from handlers.progress import progress_router
from handlers.assistant import assistant_router
from handlers.settings import settings_router
from handlers.tools import tools_router
from handlers.leaderboard import leaderboard_router
from handlers.support import support_router

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

async def handle_health_check(request):
    return web.Response(text="OK", status=200)

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle_health_check)
    app.router.add_get("/health", handle_health_check)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.getenv("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    logging.info(f"Health check HTTP server running on port {port}")

async def main():
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise ValueError("BOT_TOKEN environment variable is not set!")

    bot = Bot(token=token)
    dp = Dispatcher(storage=MemoryStorage())

    await db.init_db()
    await start_web_server()

    # Регистрируем роутеры strictly в нужном порядке (start_router ПЕРВЫМ)
    dp.include_router(start_router)
    dp.include_router(daily_tip_router)
    dp.include_router(workout_router)
    dp.include_router(nutrition_router)
    dp.include_router(progress_router)
    dp.include_router(assistant_router)
    dp.include_router(settings_router)
    dp.include_router(tools_router)
    dp.include_router(leaderboard_router)
    dp.include_router(support_router)

    await bot.delete_webhook(drop_pending_updates=True)
    logging.info("Repzilla Bot successfully started polling!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
