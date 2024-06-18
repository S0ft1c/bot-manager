from dotenv import load_dotenv
import os
from aiogram import Bot, Dispatcher, Router
from asyncio import run, sleep
from app import router
from loguru import logger
from multiprocessing import Process
from utils import convert_data
from mongo_db import db
import time
import datetime

load_dotenv()
TOKEN = os.environ.get('TG_BOT_TOKEN')


async def send_scheduled_messages(bot: Bot):
    while True:
        logger.debug('checking for schedule messages')
        msgs = await db.get_scheduled_messages()
        for msg in msgs:
            if convert_data(msg['time']) <= datetime.datetime.now():
                logger.debug('found scheduled message. Sending...')
                if msg['message'].get('photo', False):
                    await bot.send_photo(
                        photo=msg['message']['photo'],
                        caption=msg['message']['caption'],
                        chat_id=msg['chatid']
                    )
                elif msg['message'].get('video', False):
                    await bot.send_video(
                        video=msg['message']['video'],
                        caption=msg['message']['caption'],
                        chat_id=msg['chatid']
                    )
                else:
                    await bot.send_message(text=msg['message']['text'], chat_id=msg['chatid'])
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
