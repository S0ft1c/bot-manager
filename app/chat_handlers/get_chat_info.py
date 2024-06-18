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
            f'Somebody (not an admin) tried to access the bot logic!!! His info -> {message.from_user}')
        return
    chinf = await db.get_chat_info_by_id('-' + callback.data.split('-')[-1])

    await callback.message.edit_text(
        text=f'<b>Чат:</b> {chinf["title"]}\n<b>ID чата</b>: {chinf["_id"]}' +
        f'\n<b>В группе:</b> {chinf.get("group", "None")}',
        parse_mode='HTML',
        reply_markup=await kb.chat_info_kb(chinf["_id"], bool(chinf.get("group", False)))
    )
    logger.debug('Success: get the chat info')
    await callback.answer('')
