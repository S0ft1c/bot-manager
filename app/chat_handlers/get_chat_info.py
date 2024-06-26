from aiogram import Router, F
from aiogram.types import CallbackQuery
from utils import is_admin
from mongo_db import db
import app.keyboards as kb
from loguru import logger

router_get_chat_info = Router()


@router_get_chat_info.callback_query(F.data.contains('info'))
async def get_chat_info(callback: CallbackQuery):
    if not is_admin(callback):
        logger.warning(
            f'Somebody (not an admin) tried to access the bot logic!!! His info -> {callback.message.from_user.id}')
        return
    if callback.message.chat.type != 'private':
        return

    chinf = await db.get_chat_info_by_id('-' + callback.data.split('-')[-1])

    group_id = chinf.get("group_id", None)
    if group_id:
        group_info = await db.get_group_info_by_id(group_id)
        group_info = group_info['title']
    else:
        group_info = 'Не в группе'

    await callback.message.edit_text(
        text=f'<b>Чат:</b> {chinf["title"]}\n<b>ID чата</b>: {chinf["_id"]}' +
        f'\n<b>В группе:</b> {group_info}\n\n' +
        f'<i>Примечания</i> ➡️ \n1) Для того, чтобы постить в группы чатов надо добавить чат в группу. Сделать это можно через /group\n' +
        f'2) Для того чтобы настроить переливы чатов надо зайти в <b>приветствия</b>',
        parse_mode='HTML',
        reply_markup=await kb.chat_info_kb(chinf["_id"], chinf.get("group_id", False))
    )
    logger.debug('Success: get the chat info')
    await callback.answer('')
