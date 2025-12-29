import logging
import sys
from contextlib import asynccontextmanager

from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from fastapi import FastAPI

from config import config
from handlers import router

# Logging setup
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

# Bot and Dispatcher initialization
bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
dp.include_router(router)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Set webhook on startup
    webhook_url = f"{config.WEBHOOK_URL}{config.WEBHOOK_PATH}"
    logging.info(f"Setting webhook to {webhook_url}")
    await bot.set_webhook(
        url=webhook_url,
        allowed_updates=dp.resolve_used_update_types(),
        drop_pending_updates=True
    )
    yield
    # Delete webhook on shutdown
    await bot.delete_webhook()

app = FastAPI(lifespan=lifespan)

@app.post(config.WEBHOOK_PATH)
async def bot_webhook(update: dict):
    telegram_update = types.Update(**update)
    await dp.feed_update(bot=bot, update=telegram_update)
    return {"ok": True}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=config.WEB_SERVER_HOST, port=config.WEB_SERVER_PORT)

