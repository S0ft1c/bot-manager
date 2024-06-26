from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from utils import is_admin, convert_data
from mongo_db import db
from loguru import logger
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

router_edit_ad = Router()


class EditAd(StatesGroup):
    prev_id = State()
    ans = State()
    message = State()
    time = State()


@router_edit_ad.callback_query(F.data.contains('edit_ad'))
async def edit_ad(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback):
        logger.warning(
            f'Somebody (not an admin) tried to access the bot logic!!! His info -> {message.from_user}')
        return
    if callback.message.chat.type != 'private':
        return

    ad_id = callback.data.replace('edit_ad', '')
    await state.update_data(prev_id=ad_id)
    ad_info = await db.get_ad_by_id(ad_id)

    logger.debug(
        f'AD_INFO -> {ad_info}\nAND from user -> {callback.from_user.id}')

    await callback.bot.copy_message(
        chat_id=callback.from_user.id,
        message_id=ad_info['message']['message_id'],
        from_chat_id=ad_info['message']['from_chat_id']
    )
    await state.set_state(EditAd.ans)
    await callback.answer('')
    await callback.message.edit_text(
        text='Вот сообщение вашей рассылки. Напиши ДА (обязательно заглавными), если хотите изменить сообщение' +
        'Если менять его вы не хотите - НЕТ.'
    )


@router_edit_ad.message(EditAd.ans)
async def edit_ad_ans(message: Message, state: FSMContext):
    if not is_admin(message):
        logger.warning(
            f'Somebody (not an admin) tried to access the bot logic!!! His info -> {message.from_user}')
        return
    if message.chat.type != 'private':
        return

    if message.text == 'ДА':
        await state.set_state(EditAd.message)
        await message.answer(text='Круто. Теперь отправьте сообщение, которое вы хотите.')
    else:
        await state.clear()
        await message.answer(text='Хорошо... Все остается как было.')


@router_edit_ad.message(EditAd.message)
async def edit_ad_message(message: Message, state: FSMContext):
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
    await state.set_state(EditAd.time)
    await message.answer(
        text='Шаблон сообщения сохранен!\nТеперь введите время, когда надо отправить сообщение\n' +
        '<час>:<минута> <день>.<месяц>.<год>\t||\tПИСАТЬ НАДО ВСЕ.\n' +
        'Как пример: 12:00 01.05.2077\nНичего кроме текста в сообщении быть не должно.',
    )


@router_edit_ad.message(EditAd.time)
async def edit_ad_time(message: Message, state: FSMContext):
    if not is_admin(message):
        logger.warning(
            f'Somebody (not an admin) tried to access the bot logic!!! His info -> {message.from_user}')
        return
    if message.chat.type != 'private':
        return

    if convert_data(message.text):
        await state.update_data(time=message.text)
        ad_info = await state.get_data()
        await state.clear()
        await db.edit_ad(ad_info)
        await message.answer(text='Рассылка успешно отредактирована!')
    else:
        await message.answer(text='Некоррекный формат ввода даты... Попробуйте еще раз.')
