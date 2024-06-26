from utils import is_admin
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from loguru import logger
from mongo_db import db
import app.keyboards as kb
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

router_rep_sys = Router()


@router_rep_sys.callback_query(F.data.contains('rep_sys_inf'))
async def rep_sys_info(callback: CallbackQuery):
    if not is_admin(callback):
        logger.warning(
            f'Somebody (not an admin) tried to access the bot logic!!! His info -> {callback.message.from_user.id}')
        return
    if callback.message.chat.type != 'private':
        return

    chat_id = callback.data.replace('rep_sys_inf', '')
    rep_sys_workin = await db.get_rep_sys_workin(chat_id)
    reputation_w = await db.get_reputation_w(chat_id)
    if not reputation_w:
        reputation_w = 'Никаких'
    else:
        reputation_w = "; ".join(reputation_w)

    text = f'*Система репутации* - {"работает" if rep_sys_workin else "выключена"}\n' + \
        f'Слова, которые поднимают репутацию: {reputation_w}'

    await callback.answer('')
    await callback.message.edit_text(
        text=text,
        reply_markup=await kb.rep_sys_info(chat_id),
        parse_mode='Markdown'
    )


@router_rep_sys.callback_query(F.data.contains('rep_sys_change'))
async def rep_sys_change(callback: CallbackQuery):
    if not is_admin(callback):
        logger.warning(
            f'Somebody (not an admin) tried to access the bot logic!!! His info -> {callback.message.from_user.id}')
        return
    if callback.message.chat.type != 'private':
        return

    chat_id = callback.data.replace('rep_sys_change', '')
    await db.rep_sys_workin_change(chat_id)
    await callback.answer('')
    await callback.message.edit_text(
        text='Состояние системы репутации изменено!',
        reply_markup=await kb.back_to_rep_sys(chat_id)
    )


class AddRepW(StatesGroup):
    chat_id = State()
    rep_w = State()


@router_rep_sys.callback_query(F.data.contains('rep_w_add'))
async def rep_w_add(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback):
        logger.warning(
            f'Somebody (not an admin) tried to access the bot logic!!! His info -> {callback.message.from_user.id}')
        return
    if callback.message.chat.type != 'private':
        return

    chat_id = callback.data.replace('rep_w_add', '')
    await state.set_state(AddRepW.rep_w)
    await state.update_data(chat_id=chat_id)

    await callback.answer('')
    await callback.message.edit_text(
        text='Введите слова, которые вы хотите добавить через запятую и пробел после нее. ПРИМЕР "круто, спасибо, класс"',
        reply_markup=await kb.back_to_rep_sys(chat_id)
    )


@router_rep_sys.message(AddRepW.rep_w)
async def add_rep_w(message: Message, state: FSMContext):
    if not is_admin(message):
        logger.warning(
            f'Somebody (not an admin) tried to access the bot logic!!! His info -> {message.from_user}')
        return
    if message.chat.type != 'private':
        return

    chat_id = await state.get_data()
    chat_id = chat_id['chat_id']

    words = message.text.split(', ')
    await db.add_rep_w_to_chat(chat_id, words)
    await message.answer(
        text='Слова добавлены!',
        reply_markup=await kb.back_to_rep_sys(chat_id)
    )


class RemoveRepW(StatesGroup):
    chat_id = State()
    rep_w = State()


@router_rep_sys.callback_query(F.data.contains('rep_w_remove'))
async def rep_w_remove(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback):
        logger.warning(
            f'Somebody (not an admin) tried to access the bot logic!!! His info -> {callback.message.from_user.id}')
        return
    if callback.message.chat.type != 'private':
        return

    chat_id = callback.data.replace('rep_w_remove', '')
    await state.update_data(chat_id=chat_id)
    await state.set_state(RemoveRepW.rep_w)

    await callback.answer('')
    await callback.message.edit_text(
        text='Введите слова, которые вы хотите убрать через запятую и пробел после нее. ПРИМЕР "круто, спасибо, класс"',
        reply_markup=await kb.back_to_rep_sys(chat_id)
    )


@router_rep_sys.message(RemoveRepW.rep_w)
async def rep_w_remove_aa(message: Message, state: FSMContext):
    if not is_admin(message):
        logger.warning(
            f'Somebody (not an admin) tried to access the bot logic!!! His info -> {message.from_user}')
        return
    if message.chat.type != 'private':
        return

    chat_id = await state.get_data()
    chat_id = chat_id['chat_id']

    words = message.text.split(', ')
    await db.remove_rep_w_from_chat(chat_id, words)
    await message.answer(
        text='Слова удалены!',
        reply_markup=await kb.back_to_rep_sys(chat_id)
    )
