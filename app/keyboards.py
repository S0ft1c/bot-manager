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


async def chat_info_kb(chatid: str, group_id):

    # create a send posts
    rassilka = [InlineKeyboardButton(
        text='Рассылка ТОЛЬКО в чат', callback_data='rass_chat' + str(chatid))]
    if group_id:
        group_title = await db.get_group_info_by_id(group_id)
        rassilka.append(InlineKeyboardButton(
            text='Рассылка в группу чатов', callback_data='rass_group' + str(chatid)))

    builder = InlineKeyboardMarkup(
        inline_keyboard=[
            rassilka,
        ],
    )
    return builder


async def group_kb(groups):
    builder = InlineKeyboardBuilder()

    for el in groups:
        builder.add(
            InlineKeyboardButton(
                text=el['title'], callback_data='group_inf' + str(el['_id']))
        )
        builder.add(
            InlineKeyboardButton(
                text='Удалить', callback_data='del_group' + str(el['_id']))
        )
    builder.add(InlineKeyboardButton(
        text='Добавить группу', callback_data='add_group'))
    return builder.adjust(2).as_markup()


async def group_info_kb(chats, group_id):
    builder = InlineKeyboardBuilder()

    for el in chats:
        builder.add(
            InlineKeyboardButton(
                text=el['title'], callback_data='info' + str(el['_id'])),
        )
        builder.add(
            InlineKeyboardButton(
                text='Удалить чат', callback_data='del_chat_from_group' + str(el['_id']))
        )
    builder.add(
        InlineKeyboardButton(text='Добавить новый чат в группу',
                             callback_data='add_new_chat_to_group' + str(group_id))
    )
    return builder.adjust(2).as_markup()


async def add_chat_to_group_kb(chats, group_id):
    builder = InlineKeyboardBuilder()

    for el in chats:
        builder.add(InlineKeyboardButton(
            text=el['title'], callback_data='add_chat_to_group_action' +
            str(el['_id']) + ':' + group_id
        ))
    return builder.adjust(1).as_markup()


async def get_all_ads(ads):
    builder = InlineKeyboardBuilder()

    for ad in ads:
        builder.add(InlineKeyboardButton(
            text=ad['time'], callback_data='edit_ad' + str(ad['_id'])
        ))
        builder.add(InlineKeyboardButton(
            text='Удалить рассылку', callback_data='del_ad' + str(ad['_id'])
        ))
    return builder.adjust(2).as_markup()
