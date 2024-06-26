from utils import is_admin
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from mongo_db import db
from loguru import logger
import app.keyboards as kb

router_spam_add_w = Router()


class AddSpamW(StatesGroup):
    chat_id = State()
    spam_w = State()


@router_spam_add_w.callback_query(F.data.contains('add_spam_w'))
async def add_spam_w(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback):
        logger.warning(
            f'Somebody (not an admin) tried to access the bot logic!!! His info -> {callback.from_user}')
        return
    if callback.message.chat.type != 'private':
        return

    chat_id = callback.data.replace('add_spam_w', '')
    await state.update_data(chat_id=chat_id)

    await state.set_state(AddSpamW.spam_w)
    await callback.answer('')
    await callback.message.edit_text(
        text='Добавление новых спам слов. Введите слова через запятую, сколько хотите.\n' +
        'Как пример: _плохое,плохо,бесит,блин_',
        parse_mode='Markdown',
        reply_markup=await kb.back_to_spam_settings_chat(chat_id)
    )


@router_spam_add_w.message(AddSpamW.spam_w)
async def add_spam_w_2(message: Message, state: FSMContext):
    if message.chat.type != 'private':
        return
    if not is_admin(message):
        logger.warning(
            f'Somebody (not an admin) tried to access the bot logic!!! His info -> {message.from_user}')
        return

    words = message.text.split(',')
    chat_id = await state.get_data()
    chat_id = chat_id['chat_id']
    await db.add_spam_w_to_chat(chat_id, words)
    await message.answer(text='Слова успешно добавлены!',
                         reply_markup=await kb.back_to_spam_settings_chat(chat_id))
    await state.clear()
