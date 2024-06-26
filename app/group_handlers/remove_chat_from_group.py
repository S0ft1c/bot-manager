from aiogram import Router, F
from aiogram.types import CallbackQuery
from utils import is_admin
from mongo_db import db
from loguru import logger

router_remove_chat_from_group = Router()


@router_remove_chat_from_group.callback_query(F.data.contains('del_chat_from_group'))
async def remove_chat_from_group(callback: CallbackQuery):
    if not is_admin(callback):
        logger.warning(
            f'Somebody (not an admin) tried to access the bot logic!!! His info -> {callback.message.from_user}')
        return

    chat_id = callback.data.replace('del_chat_from_group', '')
    await db.remove_chat_from_group(chat_id)
    await callback.answer('')

    await callback.message.edit_text(text='Чат успешно удален из группы!')
