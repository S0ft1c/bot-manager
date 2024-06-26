from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import BaseMiddleware
from asyncio import sleep
from utils import is_admin, convert_data
from mongo_db import db
from datetime import *
from loguru import logger

router_send_messages = Router()


class SendChat(StatesGroup):
    chatid = State()
    message = State()
    time = State()


@router_send_messages.callback_query(F.data.contains('rass_chat'))
async def rass_chat(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback):
        logger.warning(
            f'Somebody (not an admin) tried to access the bot logic!!! His info -> {message.from_user}')
        return
    if callback.message.chat.type != 'private':
        return

    await state.set_state(SendChat.chatid)
    await state.update_data(chatid=int('-' + callback.data.split('-')[-1]))
    await state.set_state(SendChat.message)

    await callback.message.edit_text(
        text='<i>Производится отправка сообщения ТОЛЬКО в чат.</i>\n' +
        'Отправьте мне сообщение, которое вы хотите отправить.',
        parse_mode='HTML'
    )
    await callback.answer('')


@router_send_messages.message(SendChat.message)
async def rass_chat_msg(message: Message, state: FSMContext):
    if not is_admin(message):
        logger.warning(
            f'Somebody (not an admin) tried to access the bot logic!!! His info -> {message.from_user}')
        return
    if message.chat.type != 'private':
        return

    await state.update_data(message={
        'message_id': message.message_id,
        'from_chat_id': message.chat.id,
    })

    await message.answer(
        text='Шаблон сообщения сохранен!\nТеперь введите время, когда надо отправить сообщение\n' +
        '<час>:<минута> <день>.<месяц>.<год>\t||\tПИСАТЬ НАДО ВСЕ.\n' +
        'Как пример: 12:00 01.05.2077\nНичего кроме текста в сообщении быть не должно.',
    )
    await state.set_state(SendChat.time)


@router_send_messages.message(SendChat.time)
async def rass_chat_time(message: Message, state: FSMContext):
    if not is_admin(message):
        logger.warning(
            f'Somebody (not an admin) tried to access the bot logic!!! His info -> {message.from_user}')
        return
    if message.chat.type != 'private':
        return

    # check for good pattern
    if convert_data(message.text):
        await state.update_data(time=message.text)
        sender_data = await state.get_data()
        await state.clear()
        await db.schedule_message(sender_data)  # schedule message
        await message.answer(text='Рассылка успешно добавлена!')
    else:
        await message.answer(text='Неправильный формат сообщения!')

# FOR GROUP ---------------------------------------------------------


class SendGroup(StatesGroup):
    group_id = State()
    message = State()
    time = State()


@router_send_messages.callback_query(F.data.contains('rass_group'))
async def rass_group(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback):
        logger.warning(
            f'Somebody (not an admin) tried to access the bot logic!!! His info -> {message.from_user}')
        return
    if callback.message.chat.type != 'private':
        return

    await state.set_state(SendGroup.group_id)
    await state.update_data(
        group_id=await db.get_group_by_chat_id(int('-' + callback.data.split('-')[-1]))
    )
    await state.set_state(SendGroup.message)

    await callback.message.edit_text(
        text='<i>Производится отправка сообщения ТОЛЬКО в чат.</i>\n' +
        'Отправьте мне сообщение, которое вы хотите отправить.',
        parse_mode='HTML'
    )
    await callback.answer('')


@router_send_messages.message(SendGroup.message)
async def rass_group_msg(message: Message, state: FSMContext):
    if not is_admin(message):
        logger.warning(
            f'Somebody (not an admin) tried to access the bot logic!!! His info -> {message.from_user}')
        return
    if message.chat.type != 'private':
        return

    await state.update_data(message={
        'message_id': message.message_id,
        'from_chat_id': message.chat.id,
    })

    await message.answer(
        text='Шаблон сообщения сохранен!\nТеперь введите время, когда надо отправить сообщение\n' +
        '<час>:<минута> <день>.<месяц>.<год>\t||\tПИСАТЬ НАДО ВСЕ.\n' +
        'Как пример: 12:00 01.05.2077\nНичего кроме текста в сообщении быть не должно.',
    )
    await state.set_state(SendGroup.time)


@ router_send_messages.message(SendGroup.time)
async def rass_group_time(message: Message, state: FSMContext):
    if not is_admin(message):
        logger.warning(
            f'Somebody (not an admin) tried to access the bot logic!!! His info -> {message.from_user}')
        return
    if message.chat.type != 'private':
        return

    # check for good pattern
    if convert_data(message.text):
        await state.update_data(time=message.text)
        sender_data = await state.get_data()
        await state.clear()
        await db.schedule_message(sender_data)  # schedule message
        await message.answer(text='Рассылка успешно добавлена!')
    else:
        await message.answer(text='Неправильный формат сообщения!')
