from aiogram import Router, F
from utils import is_admin
from aiogram.types import CallbackQuery, Message
from mongo_db import db
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


class ChangeMessage(StatesGroup):
    chat_id = State()
    message = State()


router_hi_message_change = Router()


@router_hi_message_change.callback_query(F.data.contains('hi_message_change'))
async def hi_message_change(callback: CallbackQuery, state: FSMContext):
    chat_id = callback.data.replace('hi_message_change', '')
    hi_config = await db.get_hi_config(chat_id)

    text = f'Текущий текст сообщения:\n{hi_config.get('messsage', 'тут пусто...')}\n' + \
        f'Введите свой текст, чтобы изменить этот. Используйте `%username%`, чтобы вставить имя пользователя.'

    await state.update_data(chat_id=chat_id)
    await state.set_state(ChangeMessage.message)

    await callback.answer('')
    await callback.message.answer(
        text=text,
    )


@router_hi_message_change.message(ChangeMessage.message)
async def hi_change_message_2(message: Message, state: FSMContext):
    chat_id = await state.get_data()
    chat_id = chat_id['chat_id']

    msg = message.text

    await db.change_hi_message(chat_id, msg)

    await message.answer(
        text='Сообщение успешно изменено'
    )
