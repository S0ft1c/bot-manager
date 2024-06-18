from dotenv import load_dotenv
import os
from aiogram import Bot, Dispatcher, Router
from asyncio import run
from app import router
from loguru import logger

load_dotenv()
TOKEN = os.environ.get('TG_BOT_TOKEN')


async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(router=router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    logger.info('Bot deplyed!')
    run(main())
