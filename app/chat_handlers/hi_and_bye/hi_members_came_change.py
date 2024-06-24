from aiogram import Router, F
from utils import is_admin
from aiogram.types import CallbackQuery, Message
from mongo_db import db
import app.keyboards as kb
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

router_members_came_change = Router()


class MembersChange(StatesGroup):
    chat_id = State()
    cnt = State()


@router_members_came_change.callback_query(F.data.contains('hi_members_came_change'))
async def hi_members_came_change(callback: CallbackQuery, state: FSMContext):
    chat_id = callback.data.replace('hi_members_came_change', '')
    text = 'Введите количество людей, котое должен привести пользователь'

    await state.update_data(chat_id=chat_id)
    await state.set_state(MembersChange.cnt)

    await callback.answer('')
    await callback.message.answer(
        text=text
    )


@router_members_came_change.message(MembersChange.cnt)
async def hi_members_came_change_2(message: Message, state: FSMContext):
    chat_id = await state.get_data()
    chat_id = chat_id['chat_id']

    try:
        cnt = int(message.text)
        await db.update_members_change(chat_id, cnt)

        await message.answer(
            text='Количество людей обновлено!'
        )
    except Exception as e:
        await message.answer(
            text=f'Что-то пошло не так...\n`{e}`\nПопробуйте еще раз',
            parse_mode='Markdown'
        )
