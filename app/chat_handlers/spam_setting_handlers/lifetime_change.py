from utils import is_admin
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from mongo_db import db
from loguru import logger

router_lifetime_change = Router()


class LifetimeChange(StatesGroup):
    chat_id = State()
    secs = State()


@router_lifetime_change.callback_query(F.data.contains('spam_time_life'))
async def spam_time_life(callback: CallbackQuery, state: FSMContext):
    if callback.message.chat.type != 'private':
        return
    if not is_admin(callback):
        logger.warning(
            f'Somebody (not an admin) tried to access the bot logic!!! His info -> {callback.from_user}')
        return

    chat_id = callback.data.replace('spam_time_life', '')
    await state.update_data(chat_id=chat_id)

    await callback.answer('')
    await callback.message.answer(
        text='Прекрасно! Теперь укажите сколько будут жить сообщения в *СЕКУНДАХ*',
        parse_mode='Markdown'
    )
    await state.set_state(LifetimeChange.secs)


@router_lifetime_change.message(LifetimeChange.secs)
async def spam_life_time_secs(message: Message, state: FSMContext):
    if not is_admin(message):
        logger.warning(
            f'Somebody (not an admin) tried to access the bot logic!!! His info -> {message.from_user}')
        return
    if message.chat.type != 'private':
        return

    try:
        chat_id = await state.get_data()
        chat_id = chat_id['chat_id']

        secs = int(message.text)
        await db.update_secs_in_chat(chat_id, secs)
        await message.answer(text='Время жизни обновлено!')
    except Exception as e:
        await message.answer(text='Неверный формат секунд(')
