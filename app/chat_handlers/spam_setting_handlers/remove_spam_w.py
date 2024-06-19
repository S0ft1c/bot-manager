from utils import is_admin
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from mongo_db import db

router_remove_spam_w = Router()


class RemoveSpamW(StatesGroup):
    chat_id = State()
    words = State()


@router_remove_spam_w.callback_query(F.data.contains('remove_spam_w'))
async def remove_spam_w(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback):
        logger.warning(
            f'Somebody (not an admin) tried to access the bot logic!!! His info -> {callback.from_user}')
        return
    if callback.message.chat.type != 'private':
        return

    chat_id = callback.data.replace('remove_spam_w', '')
    await state.update_data(chat_id=chat_id)
    await state.set_state(RemoveSpamW.words)

    await callback.answer('')
    await callback.message.answer(
        text='Теперь введите слова, которые вы хотите удалить через запятую',
    )


@router_remove_spam_w.message(RemoveSpamW.words)
async def remove_spam_w_2(message: Message, state: FSMContext):
    if not is_admin(message):
        logger.warning(
            f'Somebody (not an admin) tried to access the bot logic!!! His info -> {message.from_user}')
        return
    if message.chat.type != 'private':
        return

    words = message.text.split(',')
    chat_id = await state.get_data()
    chat_id = chat_id['chat_id']

    await db.remove_spam_w_from_chat(chat_id, words)
    await message.answer(text='Слова были успешно удалены!')
