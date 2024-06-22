from mongo_db import db
from aiogram.types import Message
from asyncio import sleep


async def wait_for_deletion(message: Message):
    tt_sleep = await db.get_secs(message.chat.id)
    await sleep(tt_sleep)
    await message.bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id
    )
