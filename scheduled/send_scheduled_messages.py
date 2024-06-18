from asyncio import sleep
from mongo_db import db
from loguru import logger
from aiogram import Bot
from utils import convert_data
import datetime
from .chat_sender import chat_sender
from .group_sender import group_sender


async def send_scheduled_messages(bot: Bot):
    await sleep(15)
    while True:
        logger.debug('checking for schedule messages')
        msgs = await db.get_scheduled_messages()
        if msgs:  # what a shame... I like it
            for msg in msgs:
                if convert_data(msg['time']) <= datetime.datetime.now():
                    logger.debug('found scheduled message. Sending...')
                    if not msg.get('group_id', False):
                        await chat_sender(bot, msg)
                    else:
                        await group_sender(bot, msg)
        await sleep(60 * 5)  # every 5 minutes
