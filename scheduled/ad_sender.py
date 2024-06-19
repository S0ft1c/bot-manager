from aiogram import Bot
from mongo_db import db


async def ad_sender(bot: Bot, msg):
    chats = await db.get_chats()
    for ch in chats:
        await bot.copy_message(
            chat_id=ch['_id'],
            from_chat_id=msg['message']['from_chat_id'],
            message_id=msg['message']['message_id']
        )
    await db.delete_schedule_message_by_obj_id(msg['_id'])
