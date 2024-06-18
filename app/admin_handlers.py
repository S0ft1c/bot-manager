from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from loguru import logger
from utils import is_admin
from mongo_db import db
import app.keyboards as kb

router_admin_handlers = Router()


@router_admin_handlers.message(CommandStart())
async def command_start(message: Message):
    if not is_admin(message):
        logger.warning(
            f'Somebody (not an admin) tried to access the bot logic!!! His info -> {message.from_user}')
        return

    await message.answer(
        text=f"""Здравствуйте, {message.from_user.first_name}!
Внизу вы видите кнопки, каждая из которых соответствует одному из ваших чатов.
Чтобы бот начал работать в выбранном чате, выполните следующие шаги:
1) Добавьте бота в чат. ➕
2) Назначьте бота администратором.
3) В чате отправьте команду /add_exec, либо в лс бота /add <id чата>.""",
        reply_markup=await kb.start_kb()
    )


@router_admin_handlers.message(Command('add'))
async def command_add_group(message: Message):
    if not is_admin(message):
        logger.warning(
            f'Somebody (not an admin) tried to access the bot logic!!! His info -> {message.from_user}')
        return

    chat_id = message.text.split()[-1]
    chat_inf = {
        '_id': chat_id,
        'title': chat_id,  # FIXME: заглушка по title группы, зная только ее id
    }
    ress = await db.insert_chat(chat_inf)

    if ress is None:
        await message.answer(text='Произошла ошибка при добавлении...')
    elif not ress:
        await message.answer(text='Такой чат уже есть!')
    else:
        await message.answer(text='Чат успешно добавлен!')


@router_admin_handlers.message(Command('add_exec'))
async def command_add_exec(message: Message):
    if not is_admin(message):
        logger.warning(
            f'Somebody (not an admin) tried to access the bot logic!!! His info -> {message.from_user}')
        return

    if message.chat.type == 'private':
        await message.answer('Данная команда должна быть написана непосредственно в группе!')
    else:
        print(message)
        chat_inf = {
            '_id': message.chat.id,
            'title': message.chat.title,
        }
        ress = await db.insert_chat(chat_inf)

        if ress is None:
            await message.answer(text='Произошла ошибка при добавлении...')
        elif not ress:
            await message.answer(text='Такой чат уже есть!')
        else:
            await message.answer(text='Чат успешно добавлен!')
