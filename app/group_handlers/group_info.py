from aiogram import Router, F
from aiogram.types import CallbackQuery
from mongo_db import db
import app.keyboards as kb
from utils import is_admin
from loguru import logger

router_group_info = Router()


@router_group_info.callback_query(F.data.contains('group_inf'))
async def group_info_handler(callback: CallbackQuery):
    if not is_admin(callback):
        logger.warning(
            f'Somebody (not an admin) tried to access the bot logic!!! His info -> {message.from_user}')
        return

    group_id = callback.data.replace('group_inf', '')
    logger.debug(f'the group_id is {group_id}')
    group = await db.get_group_info_by_id(group_id)
    chats = await db.get_all_chats_from_group_by_id(group_id)

    await callback.message.answer(
        text=f'Группа чатов: {group['title']}',
        reply_markup=await kb.group_info_kb(chats, group_id)
    )
