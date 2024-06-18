from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from utils import is_admin
from mongo_db import db
from loguru import logger


router_create_group = Router()


class AddGroup(StatesGroup):
    title = State()


@router_create_group.callback_query(F.data == 'add_group')
async def add_group_handler(callback: CallbackQuery, state: FSMContext):
    logger.debug('Adding group...')
    if not is_admin(callback):
        logger.warning(
            f'Somebody (not an admin) tried to access the bot logic!!! His info -> {message.from_user}')
        return

    await callback.message.answer(text='Введите название группы')
    await state.set_state(AddGroup.title)


@router_create_group.message(AddGroup.title)
async def add_group_title(message: Message, state: FSMContext):
    if not is_admin(message):
        logger.warning(
            f'Somebody (not an admin) tried to access the bot logic!!! His info -> {message.from_user}')
        return

    await db.create_group(message.text)
    await message.answer(text='Группа успешно добавлена!')
