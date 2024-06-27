from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message, CallbackQuery
from loguru import logger
from utils import is_admin
from mongo_db import db
import app.keyboards as kb
from asyncio import sleep

router_admin_handlers = Router()


@router_admin_handlers.message(CommandStart(deep_link=False))
async def command_start(message: Message, command: CommandObject):
    if not is_admin(message):
        print(message.text, command)
        logger.error('oooooohh')
        args = command.args
        chat_id, user_id = args.split('00000')
        event_user_id = message.from_user.id
        logger.info(chat_id, user_id)
        await db.ref_user_came(chat_id, user_id, event_user_id)

        ch_info = await db.get_chat_info_by_id(chat_id)
        link = await message.bot.create_chat_invite_link(chat_id=chat_id)
        await message.answer(
            text='Пожалуйста перейдите по ссылке в группу!',
            reply_markup=await kb.start_kbkkbkb(ch_info.get('link', link))
        )
        return

    if message.chat.type != 'private':
        return

    logger.error('yay')
    await message.answer(
        text=f"""Здравствуйте, {message.from_user.first_name}! 👋
Внизу вы видите кнопки, каждая из которых соответствует одному из ваших чатов. 🗂️
Чтобы бот начал работать в выбранном чате, выполните следующие шаги:
1️⃣ Добавьте бота в чат. ➕
2️⃣ Назначьте бота администратором. 👑
3️⃣ В чате отправьте команду /add_exec, либо в лс бота /add <id чата>. 📝

Также можете просмотреть группы при помощи /group
""",
        reply_markup=await kb.start_kb()
    )


@router_admin_handlers.message(CommandStart(deep_link=True))
async def command_start(message: Message, command: CommandObject):
    if not is_admin(message):
        print(message.text, command)
        logger.error('oooooohh')
        args = command.args
        chat_id, user_id = args.split('00000')
        logger.info(chat_id, user_id)
        await db.ref_user_came(chat_id, user_id)

        ch_info = await db.get_chat_info_by_id(chat_id)
        link = await message.bot.create_chat_invite_link(chat_id=chat_id)
        await message.answer(
            text='Пожалуйста перейдите по ссылке в группу!',
            reply_markup=await kb.start_kbkkbkb(ch_info.get('link', link))
        )
        return

    if message.chat.type != 'private':
        return

    logger.error('yay')
    await message.answer(
        text=f"""Здравствуйте, {message.from_user.first_name}! 👋
Внизу вы видите кнопки, каждая из которых соответствует одному из ваших чатов. 🗂️
Чтобы бот начал работать в выбранном чате, выполните следующие шаги:
1️⃣ Добавьте бота в чат. ➕
2️⃣ Назначьте бота администратором. 👑
3️⃣ В чате отправьте команду /add_exec, либо в лс бота /add <id чата>. 📝

Также можете просмотреть группы при помощи /group
""",
        reply_markup=await kb.start_kb()
    )


@router_admin_handlers.message(Command('add'))
async def command_add_group(message: Message):
    if not is_admin(message):
        logger.warning(
            f'Somebody (not an admin) tried to access the bot logic!!! His info -> {message.from_user}')
        return
    if message.chat.type != 'private':
        return
    try:
        chat_id = message.text.split()[-1]

        chat_inf = {
            '_id': int(chat_id),
            'title': chat_id,  # FIXME: заглушка по title группы, зная только ее id
        }
        ress = await db.insert_chat(chat_inf)

        if ress is None:
            await message.answer(text='Произошла ошибка при добавлении...')
        elif not ress:
            await message.answer(text='Такой чат уже есть!')
        else:
            await message.answer(text='Чат успешно добавлен!')
    except:
        await message.answer(text='Произошла ошибка при добавлении...')


@router_admin_handlers.callback_query(F.data.contains('ddd_chat'))
async def ddd_chat(callback: CallbackQuery):
    chat_id = callback.data.replace('ddd_chat', '')
    await db.delete_chat_by_id(chat_id)

    await callback.answer('')
    await callback.message.answer(
        text='Чат успешно удален!'
    )


@router_admin_handlers.message(Command('add_exec'))
async def command_add_exec(message: Message):
    if not is_admin(message):
        logger.warning(
            f'Somebody (not an admin) tried to access the bot logic!!! His info -> {message.from_user}')
        return

    try:

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
                result_message = await message.answer(text='Произошла ошибка при добавлении...')
            elif not ress:
                result_message = await message.answer(text='Такой чат уже есть!')
            else:
                result_message = await message.answer(text='Чат успешно добавлен!')
            await sleep(3)
            await result_message.delete()
            await message.delete()
    except:
        await message.answer(text='Произошла ошибка при добавлении...')


@router_admin_handlers.message(Command('test'))
async def test(message: Message):
    if not is_admin(message):
        logger.warning(
            f'Somebody (not an admin) tried to access the bot logic!!! His info -> {message.from_user}')
        return
    if message.chat.type != 'private':
        return

    print(message)
    await message.answer('Смотри в консоль)')
    await sleep(10)
    await message.answer('Sleep awaited')


@router_admin_handlers.message(Command('group'))
async def command_group(message: Message):
    if not is_admin(message):
        logger.warning(
            f'Somebody (not an admin) tried to access the bot logic!!! His info -> {message.from_user}')
        return
    if message.chat.type != 'private':
        return

    groups = await db.get_group_names()
    text = 'Ваши группы:\n\n'
    for idx, el in enumerate(groups):
        text += f'{idx + 1}) {el["title"]}: {";".join(
            i['title'] for i in await db.get_all_chats_from_group_by_id(el["_id"]))}\n'

    await message.answer(
        text=text,
        reply_markup=await kb.group_kb(groups)
    )
