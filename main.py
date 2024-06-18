from dotenv import load_dotenv
import os
from aiogram import Bot, Dispatcher, Router
from aiogram.utils.media_group import MediaGroupBuilder
from asyncio import run, sleep
from app import router
from loguru import logger
from multiprocessing import Process
from utils import convert_data
from mongo_db import db, DB
import time
import datetime

load_dotenv()
TOKEN = os.environ.get('TG_BOT_TOKEN')


async def send_scheduled_messages(bot: Bot):
    await sleep(15)
    while True:
        logger.debug('checking for schedule messages')
        msgs = await db.get_scheduled_messages()
        if msgs:
            for msg in msgs:
                if convert_data(msg['time']) <= datetime.datetime.now():
                    logger.debug('found scheduled message. Sending...')
                    await bot.copy_message(
                        chat_id=msg['chatid'],
                        from_chat_id=msg['message']['from_chat_id'],
                        message_id=msg['message']['message_id']
                    )
                    await db.delete_schedule_message_by_id(msg['chatid'])
        await sleep(60 * 5)  # every 5 minutes


def schedule_worker(bot):
    run(send_scheduled_messages(bot))


async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    process = Process(target=schedule_worker,
                      args=[bot])  # for scheduled messages
    process.start()

    dp.include_router(router=router)
    await dp.start_polling(bot)

    process.join()  # for scheduled messages


if __name__ == '__main__':
    logger.info('Bot deplyed!')
    run(main())
