from utils import is_admin
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from mongo_db import db
from loguru import logger

router_warn_user = Router()


@router_warn_user.message(Command('warn_user'))
async def warn_user(message: Message):
    if not is_admin(message):
        logger.warning(
            f'Somebody (not an admin) tried to access the bot logic!!! His info -> {message.from_user}')
        return
    if message.chat.type not in ['group', 'supergroup']:
        return

    if message.reply_to_message:
        man = message.reply_to_message.from_user.id
        await db.add_warn_to_user(man)

        chat_id = message.chat.id
        await message.answer(
            text=await db.get_text_conf(chat_id, 'warn')
        )
    else:
        await message.answer(
            text='Выполните команду в ответ на сообщение пользователя, которого надо предупредить'
        )
