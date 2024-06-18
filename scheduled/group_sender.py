from mongo_db import db
from aiogram import Bot


async def group_sender(bot: Bot, msg):
    chats = await db.get_all_chats_from_group_by_id(msg['group_id'])
    for chat in chats:
        await bot.copy_message(
            chat_id=int(chat['_id']),
            from_chat_id=msg['message']['from_chat_id'],
            message_id=msg['message']['message_id']
        )
        await db.delete_schedule_message_by_group_id(msg['group_id'])
