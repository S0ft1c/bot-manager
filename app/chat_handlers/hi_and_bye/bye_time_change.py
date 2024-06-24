from aiogram import Router, F
from utils import is_admin
from aiogram.types import CallbackQuery, Message
from mongo_db import db
import app.keyboards as kb
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

router_bye_time_change = Router()


class ByeTimeChange(StatesGroup):
    chat_id = State()
    sleep_time = State()


@router_bye_time_change.callback_query(F.data.contains('bye_time_change'))
async def bye_time_change(callback: CallbackQuery, state: FSMContext):
    chat_id = callback.data.replace('bye_time_change', '')
    text = 'Введите время до удаления прощального сообщения в секундах'

    await state.update_data(chat_id=chat_id)
    await state.set_state(ByeTimeChange.sleep_time)

    await callback.answer('')
    await callback.message.answer(
        text=text
    )


@router_bye_time_change.message(ByeTimeChange.sleep_time)
async def bye_time_change_2(message: Message, state: FSMContext):
    chat_id = await state.get_data()
    chat_id = chat_id['chat_id']

    try:
        sleep_time = int(message.text)
        await db.update_bye_sleep_time(chat_id, sleep_time)

        await message.answer(
            text='Время обновлено!'
        )
    except Exception as e:
        await message.answer(
            text=f'Что-то пошло не так...\n`{e}`\nПопробуйте еще раз',
            parse_mode='Markdown'
        )
