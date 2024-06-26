from utils import is_admin
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from mongo_db import db
from loguru import logger
import app.keyboards as kb


router_delete_posts = Router()


class DelPosts(StatesGroup):
    chat_id = State()
    user = State()


@router_delete_posts.callback_query(F.data.contains('delete_posts'))
async def delete_posts(callback: CallbackQuery, state: FSMContext):
    if callback.message.chat.type != 'private':
        return
    if not is_admin(callback):
        logger.warning(
            f'Somebody (not an admin) tried to access the bot logic!!! His info -> {callback.from_user}')
        return

    chat_id = callback.data.replace('delete_posts', '')
    await state.update_data(chat_id=chat_id)
    await state.set_state(DelPosts.user)

    await callback.answer('')
    await callback.message.edit_text(
        text='Теперь введите id пользователя, сообщения которого вы хотите удалить.',
        reply_markup=await kb.back_to_info(chat_id)
    )


@router_delete_posts.message(DelPosts.user)
async def delete_posts_user(message: Message, state: FSMContext):
    if not is_admin(message):
        logger.warning(
            f'Somebody (not an admin) tried to access the bot logic!!! His info -> {message.from_user}')
        return
    if message.chat.type != 'private':
        return
    chat_id = await state.get_data()
    chat_id = chat_id['chat_id']

    try:
        await state.clear()
        users_messages = await db.get_users_messages_for_del(chat_id=chat_id, user_id=message.text)
        for msg in users_messages:
            await message.bot.delete_message(
                chat_id=chat_id,
                message_id=msg['message_id']
            )
        await message.answer(
            text='Удаление прошло успешно!',
            reply_markup=await kb.back_to_info(chat_id)
        )
    except Exception as e:
        await message.answer(
            text=f'Что-то пошло не так... -> {e}',
            reply_markup=await kb.back_to_info(chat_id)
        )
