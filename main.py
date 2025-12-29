import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import config
from handlers import router

# Logging setup
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

# Bot and Dispatcher initialization
bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
dp.include_router(router)

async def main():
    # Delete webhook to ensure polling works
    await bot.delete_webhook(drop_pending_updates=True)
    logging.info("Starting bot in polling mode...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Bot stopped")

