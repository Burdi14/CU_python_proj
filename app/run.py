import os
import asyncio
import logging
from bot import bot, dp
from aiogram.utils.chat_action import ChatActionMiddleware
from handlers import router

logging.basicConfig(level=logging.INFO)

async def main():
    dp.include_router(router)
    dp.message.middleware(ChatActionMiddleware())

    logging.info("Bot polling started.")
    await dp.start_polling(bot)

if __name__ == "__main__":

    asyncio.run(main())
