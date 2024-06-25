from aiogram import Router, F
from utils import is_admin
from aiogram.types import CallbackQuery, Message
from mongo_db import db
import app.keyboards as kb
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

router_hi_pereliv_chanells_menu = Router()


class AddChannel(StatesGroup):
    chat_id = State()
    link = State()


@router_hi_pereliv_chanells_menu.callback_query(F.data.contains('hi_pereliv_chanells_menu'))
async def hi_pereliv_chanells_menu(callback: CallbackQuery, state: FSMContext):
    chat_id = callback.data.replace('hi_pereliv_chanells_menu', '')

    await state.update_data(chat_id=chat_id)
    await state.set_state(AddChannel.link)

    hi_config = await db.get_hi_config(chat_id)
    channels = hi_config.get('channels', [])

    text = f'Вот каналы, которые сейчас прикреплены:\n{"\n".join(channels)}\n\n' + \
        'Если хотите добавить еще канал - просто напишите id канала'

    await callback.answer('')
    await callback.message.answer(
        text=text,
        reply_markup=await kb.hi_pereliv_chanells(channels)
    )


@router_hi_pereliv_chanells_menu.message(AddChannel.link)
async def hi_pereliv_chanells_menu_link(message: Message, state: FSMContext):
    chat = await state.get_data()
    chat_id = chat['chat_id']
    await state.update_data(chat_id=chat_id)

    await db.add_channel_to_hi(chat_id, message.text)

    await message.answer(
        text='Ссылка успешно добавлена!'
    )


@router_hi_pereliv_chanells_menu.callback_query(F.data.contains('hi_del_channel'))
async def hi_del_channel(callback: CallbackQuery, state: FSMContext):
    link = callback.data.replace('hi_del_channel', '')
    chat = await state.get_data()
    chat_id = chat['chat_id']
    await state.update_data(chat_id=chat_id)

    await db.rmv_channel_from_hi(chat_id, link)

    await callback.answer('')
    await callback.message.answer(
        text='Ссылка успешно удалена!'
    )
