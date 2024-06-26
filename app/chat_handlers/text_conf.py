from utils import is_admin
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from loguru import logger
import app.keyboards as kb
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from mongo_db import db

router_text_conf = Router()


@router_text_conf.callback_query(F.data.contains('text_conf'))
async def text_conf(callback: CallbackQuery):
    if not is_admin(callback):
        logger.warning(
            f'Somebody (not an admin) tried to access the bot logic!!! His info -> {callback.from_user}')
        return
    if callback.message.chat.type != 'private':
        return

    chat_id = callback.data.replace('text_conf', '')
    await callback.answer('')
    await callback.message.edit_text(
        text='Выберите текст который вы хотите поменять!',
        reply_markup=await kb.text_conf_kb(chat_id)
    )

#  -- -- -- -- -- -- -- -- -- -- -- -- -- -- - -- - -- - -- - - - for warnings


class Warn(StatesGroup):
    chat_id = State()
    msg = State()


@router_text_conf.callback_query(F.data.contains('text_change_warn'))
async def text_change_warn(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback):
        logger.warning(
            f'Somebody (not an admin) tried to access the bot logic!!! His info -> {callback.from_user}')
        return
    if callback.message.chat.type != 'private':
        return

    chat_id = callback.data.replace('text_change_warn', '')
    await state.update_data(chat_id=chat_id)
    await state.set_state(Warn.msg)

    await callback.answer('')
    await callback.message.edit_text(
        text='Введите сообщение.',
        reply_markup=await kb.back_to_text_conf(chat_id)
    )


@router_text_conf.message(Warn.msg)
async def text_change_warn_msg(message: Message, state: FSMContext):
    if not is_admin(message):
        logger.warning(
            f'Somebody (not an admin) tried to access the bot logic!!! His info -> {message.from_user}')
        return
    if message.chat.type != 'private':
        return

    chat_id = await state.get_data()
    chat_id = chat_id['chat_id']
    msg = message.text
    await db.update_warn_message(chat_id, msg)

    await message.answer(text="Текст успешно обновлен!",
                         reply_markup=await kb.back_to_text_conf(chat_id))


#  -- -- -- -- -- -- -- -- -- -- -- -- -- -- - -- - -- - -- - - - for mute


class Mute(StatesGroup):
    chat_id = State()
    msg = State()


@router_text_conf.callback_query(F.data.contains('text_change_mute'))
async def text_change_mute(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback):
        logger.warning(
            f'Somebody (not an admin) tried to access the bot logic!!! His info -> {callback.from_user}')
        return
    if callback.message.chat.type != 'private':
        return

    chat_id = callback.data.replace('text_change_mute', '')
    await state.update_data(chat_id=chat_id)
    await state.set_state(Mute.msg)

    await callback.answer('')
    await callback.message.edit_text(
        text='Введите сообщение.',
        reply_markup=await kb.back_to_text_conf(chat_id)
    )


@router_text_conf.message(Mute.msg)
async def text_change_mute_msg(message: Message, state: FSMContext):
    if not is_admin(message):
        logger.warning(
            f'Somebody (not an admin) tried to access the bot logic!!! His info -> {message.from_user}')
        return
    if message.chat.type != 'private':
        return

    chat_id = await state.get_data()
    chat_id = chat_id['chat_id']
    msg = message.text
    await db.update_mute_message(chat_id, msg)

    await message.answer(text="Текст успешно обновлен!",
                         reply_markup=await kb.back_to_text_conf(chat_id))


#  -- -- -- -- -- -- -- -- -- -- -- -- -- -- - -- - -- - -- - - - for ban


class Ban(StatesGroup):
    chat_id = State()
    msg = State()


@router_text_conf.callback_query(F.data.contains('text_change_ban'))
async def text_change_ban(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback):
        logger.warning(
            f'Somebody (not an admin) tried to access the bot logic!!! His info -> {callback.from_user}')
        return
    if callback.message.chat.type != 'private':
        return

    chat_id = callback.data.replace('text_change_ban', '')
    await state.update_data(chat_id=chat_id)
    await state.set_state(Ban.msg)

    await callback.answer('')
    await callback.message.edit_text(
        text='Введите сообщение.',
        reply_markup=await kb.back_to_text_conf(chat_id)
    )


@router_text_conf.message(Ban.msg)
async def text_change_ban_msg(message: Message, state: FSMContext):
    if not is_admin(message):
        logger.warning(
            f'Somebody (not an admin) tried to access the bot logic!!! His info -> {message.from_user}')
        return
    if message.chat.type != 'private':
        return

    chat_id = await state.get_data()
    chat_id = chat_id['chat_id']
    msg = message.text
    await db.update_ban_message(chat_id, msg)

    await message.answer(text="Текст успешно обновлен!",
                         reply_markup=await kb.back_to_text_conf(chat_id))


#  -- -- -- -- -- -- -- -- -- -- -- -- -- -- - -- - -- - -- - - - for kick


class Kick(StatesGroup):
    chat_id = State()
    msg = State()


@router_text_conf.callback_query(F.data.contains('text_change_kick'))
async def text_change_kick(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback):
        logger.warning(
            f'Somebody (not an admin) tried to access the bot logic!!! His info -> {callback.from_user}')
        return
    if callback.message.chat.type != 'private':
        return

    chat_id = callback.data.replace('text_change_kick', '')
    await state.update_data(chat_id=chat_id)
    await state.set_state(Kick.msg)

    await callback.answer('')
    await callback.message.edit_text(
        text='Введите сообщение.',
        reply_markup=await kb.back_to_text_conf(chat_id)
    )


@router_text_conf.message(Kick.msg)
async def text_change_kick_msg(message: Message, state: FSMContext):
    if not is_admin(message):
        logger.warning(
            f'Somebody (not an admin) tried to access the bot logic!!! His info -> {message.from_user}')
        return
    if message.chat.type != 'private':
        return

    chat_id = await state.get_data()
    chat_id = chat_id['chat_id']
    msg = message.text
    await db.update_kick_message(chat_id, msg)

    await message.answer(text="Текст успешно обновлен!",
                         reply_markup=await kb.back_to_text_conf(chat_id))


#  -- -- -- -- -- -- -- -- -- -- -- -- -- -- - -- - -- - -- - - - for un


class Un(StatesGroup):
    chat_id = State()
    msg = State()


@router_text_conf.callback_query(F.data.contains('text_change_un'))
async def text_change_un(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback):
        logger.warning(
            f'Somebody (not an admin) tried to access the bot logic!!! His info -> {callback.from_user}')
        return
    if callback.message.chat.type != 'private':
        return

    chat_id = callback.data.replace('text_change_un', '')
    await state.update_data(chat_id=chat_id)
    await state.set_state(Un.msg)

    await callback.answer('')
    await callback.message.edit_text(
        text='Введите сообщение.',
        reply_markup=await kb.back_to_text_conf(chat_id)
    )


@router_text_conf.message(Un.msg)
async def text_change_un_msg(message: Message, state: FSMContext):
    if not is_admin(message):
        logger.warning(
            f'Somebody (not an admin) tried to access the bot logic!!! His info -> {message.from_user}')
        return
    if message.chat.type != 'private':
        return

    chat_id = await state.get_data()
    chat_id = chat_id['chat_id']
    msg = message.text
    await db.update_un_message(chat_id, msg)

    await message.answer(text="Текст успешно обновлен!",
                         reply_markup=await kb.back_to_text_conf(chat_id))
