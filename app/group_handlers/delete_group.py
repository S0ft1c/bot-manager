from aiogram import Router, F
from aiogram.types import CallbackQuery
from utils import is_admin
from mongo_db import db

router_delete_group = Router()


@router_delete_group.callback_query(F.data.contains('del_group'))
async def delete_group(callback: CallbackQuery):
    if not is_admin(callback):
        logger.warning(
            f'Somebody (not an admin) tried to access the bot logic!!! His info -> {message.from_user}')
        return

    group_id = callback.data.replace('del_group', '')
    await db.delete_group(group_id)

    await callback.message.answer(text='Группа успешно удалена!')
