from mongo_db import db


async def chat_sender(bot, msg):
    await bot.copy_message(
        chat_id=msg['chatid'],
        from_chat_id=msg['message']['from_chat_id'],
        message_id=msg['message']['message_id']
    )
    await db.delete_schedule_message_by_id(msg['chatid'])
