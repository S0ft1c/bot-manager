from aiogram import Router, F
from utils import is_admin
from aiogram.types import CallbackQuery, Message
from mongo_db import db
import app.keyboards as kb
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

router_bye_message_change = Router()


class ByeMessageChange(StatesGroup):
    chat_id = State()
    message = State()


@router_bye_message_change.callback_query(F.data.contains('bye_message_change'))
async def bye_message_change(callback: CallbackQuery, state: FSMContext):
    chat_id = callback.data.replace('bye_message_change', '')
    text = 'Введите новое прощальное сообщение. Вы можете использовать конструкцию `%username%`,' + \
        'чтобы подставить туда имя пользователя.'

    await state.update_data(chat_id=chat_id)
    await state.set_state(ByeMessageChange.message)

    await callback.answer('')
    await callback.message.edit_text(
        text=text,
        parse_mode='Markdown',
        reply_markup=await kb.back_to_bye_config(chat_id)
    )


@router_bye_message_change.message(ByeMessageChange.message)
async def bye_message_change_2(message: Message, state: FSMContext):
    chat_id = await state.get_data()
    chat_id = chat_id['chat_id']
    await state.clear()
    msg = message.text

    await db.update_bye_message(chat_id, msg)
    await message.answer(
        text='Прощальное сообщение успешно изменено!',
        reply_markup=await kb.back_to_bye_config(chat_id)
    )
