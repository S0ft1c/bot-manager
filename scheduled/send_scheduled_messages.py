from asyncio import sleep
from mongo_db import db
from loguru import logger
from aiogram import Bot
from utils import convert_data
import datetime


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
