from aiogram import Router, F
from utils import is_admin, convert_data
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from mongo_db import db

router_create_ad = Router()


class CreateAd(StatesGroup):
    message = State()
    time = State()


@router_create_ad.message(Command('create_ad'))
async def command_create_ad(message: Message, state: FSMContext):
    if not is_admin(message):
        logger.warning(
            f'Somebody (not an admin) tried to access the bot logic!!! His info -> {message.from_user}')
        return
    if message.chat.type != 'private':
        return
    await message.answer(text='Прекрасно! Создание рекламной рассылки началось. Отправьте сообщение сюда.')
    await state.set_state(CreateAd.message)


@router_create_ad.message(CreateAd.message)
async def create_ad_message_id(message: Message, state: FSMContext):
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
    await state.set_state(CreateAd.time)
    await message.answer(
        text='Шаблон сообщения сохранен!\nТеперь введите время, когда надо отправить сообщение\n' +
        '<час>:<минута> <день>.<месяц>.<год>\t||\tПИСАТЬ НАДО ВСЕ.\n' +
        'Как пример: 12:00 01.05.2077\nНичего кроме текста в сообщении быть не должно.',
    )


@router_create_ad.message(CreateAd.time)
async def create_ad_time(message: Message, state: FSMContext):
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
        await db.create_ad(ad_info)
        await message.answer(text='Реклама успешно добавлена!')
    else:
        await message.answer(text='Введенная дата не соответствует формату... Попробуйте еще раз.')
