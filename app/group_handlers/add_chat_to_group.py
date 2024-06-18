from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from mongo_db import db
import app.keyboards as kb
from utils import is_admin

router_add_chat_to_group = Router()


@router_add_chat_to_group.callback_query(F.data.contains('add_new_chat_to_group'))
async def add_new_chat_to_group(callback: CallbackQuery):
    if not is_admin(callback):
        logger.warning(
            f'Somebody (not an admin) tried to access the bot logic!!! His info -> {message.from_user}')
        return

    group_id = callback.data.replace('add_new_chat_to_group', '')
    chats = await db.get_all_nongroup_chats()

    await callback.message.answer(
        text=f'Вот список групп!', reply_markup=await kb.add_chat_to_group_kb(chats, group_id)
    )


@router_add_chat_to_group.callback_query(F.data.contains('add_chat_to_group_action'))
async def add_chat_to_group_action(callback: CallbackQuery):
    if not is_admin(callback):
        logger.warning(
            f'Somebody (not an admin) tried to access the bot logic!!! His info -> {message.from_user}')
        return

    chat_id, group_id = callback.data.replace(
        'add_chat_to_group_action', '').split(':')

    await db.add_chat_to_group_action(chat_id, group_id)
    await callback.message.answer(text='Чат успешно добавлен!')
