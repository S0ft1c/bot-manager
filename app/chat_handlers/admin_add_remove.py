from utils import is_admin
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
import app.keyboards as kb
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from loguru import logger

router_admin_add_remove = Router()
promote = {
    'can_manage_chat': True,
}
depromote = {
    'can_manage_chat': False,
}


class AddAdmin(StatesGroup):
    chat_id = State()
    user_id = State()


@router_admin_add_remove.callback_query(F.data.contains('admin_add_remove'))
async def admin_add_remove(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback):
        logger.warning(
            f'Somebody (not an admin) tried to access the bot logic!!! His info -> {callback.from_user}')
        return
    if callback.message.chat.type != 'private':
        return

    chat_id = callback.data.replace('admin_add_remove', '')
    await state.update_data(chat_id=chat_id)
    admins = await callback.bot.get_chat_administrators(
        chat_id=int(chat_id),
    )
    print(admins)

    await state.set_state(AddAdmin.user_id)
    await callback.answer('')
    await callback.message.edit_text(
        text='Введите id пользователя, которого хотите сделать администратором.\n' +
        "Или нажмите внизу на существующих, чтобы разжаловать их.",
        reply_markup=await kb.admin_add_remove(admins, chat_id)
    )


@router_admin_add_remove.message(AddAdmin.user_id)
async def admin_add_by_id(message: Message, state: FSMContext):
    if message.chat.type != 'private':
        return
    if not is_admin(message):
        logger.warning(
            f'Somebody (not an admin) tried to access the bot logic!!! His info -> {message.from_user}')
        return

    chat_id = await state.get_data()
    chat_id = chat_id['chat_id']

    try:
        await message.bot.promote_chat_member(
            chat_id=chat_id,
            user_id=message.text,
            **promote,
        )
        state.clear()
        await message.answer(
            text='Администратор успешно добавлен!'
        )
    except Exception as e:
        await message.answer(
            text=f'Ошибка... -> {e}\nМожете попробовать еще раз.',
        )


@router_admin_add_remove.callback_query(F.data.contains('delete_admin'))
async def delete_admin(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback):
        logger.warning(
            f'Somebody (not an admin) tried to access the bot logic!!! His info -> {callback.from_user}')
        return
    if callback.message.chat.type != 'private':
        return
    await state.clear()

    admin_id, chat_id = callback.data.replace('delete_admin', '').split('-')
    chat_id = '-' + chat_id

    try:
        await callback.message.bot.promote_chat_member(
            chat_id=chat_id,
            user_id=admin_id,
            **depromote
        )
        await callback.answer('')
        await callback.message.edit_text(
            text='Админ успешно понижен в звании'
        )
    except Exception as e:
        await callback.answer('')
        await callback.message.edit_text(
            text=f'Что-то пошло не так... -> {e}\nЕще раз?'
        )
