from aiogram.types import KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from mongo_db import db


async def start_kb():
    chats_info = await db.get_chats_info()
    builder = InlineKeyboardBuilder()
    for el in chats_info:
        builder.add(InlineKeyboardButton(
            text=el['title'], callback_data='info' + str(el['_id'])
        ))
    return builder.adjust(1).as_markup()


async def chat_info_kb(chatid: str, in_group: bool):

    # create a send posts
    rassilka = [InlineKeyboardButton(
        text='Рассылка ТОЛЬКО в чат', callback_data='rass_chat' + str(chatid))]
    if in_group:
        rassilka.append(InlineKeyboardButton(
            text='Рассылка в группу чатов', callback_data='rass_group' + str(chatid)))

    builder = InlineKeyboardMarkup(
        inline_keyboard=[
            rassilka,
        ],
    )
    return builder
