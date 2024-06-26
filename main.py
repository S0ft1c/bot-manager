from dotenv import load_dotenv
import os
from aiogram import Bot, Dispatcher, Router
from aiogram.utils.media_group import MediaGroupBuilder
from asyncio import run, sleep
from app import router
from loguru import logger
from multiprocessing import Process
from utils import convert_data
from mongo_db import db
import time
import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from scheduled import schedule_worker, send_scheduled_messages
from middle_ware import (MainMiddleware, AntispamMiddleware, ClearSystem,
                         ReputationSystem, HiAndByeMiddleware, AcceptMessageMiddleware)


async def main():

    load_dotenv()
    TOKEN = os.environ.get('TG_BOT_TOKEN')
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    # process = Process(target=schedule_worker,
    #                   args=[bot])  # for scheduled messages
    # process.start()
    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    scheduler.add_job(send_scheduled_messages, trigger='interval',
                      seconds=60,
                      kwargs={'bot': bot})
    scheduler.start()

    dp.message.outer_middleware(HiAndByeMiddleware())  # for hi and bye logics
    # for non great users
    dp.message.outer_middleware(AcceptMessageMiddleware())
    dp.message.outer_middleware(MainMiddleware())  # for saving to db
    dp.message.outer_middleware(AntispamMiddleware())  # for antispam defense
    # for clearing system notifications
    dp.message.outer_middleware(ClearSystem())
    dp.message.outer_middleware(ReputationSystem())  # for reputation system

    dp.include_router(router=router)
    await dp.start_polling(bot)

    # process.join()  # for scheduled messages


if __name__ == '__main__':
    logger.info('Bot deplyed!')
    run(main())
