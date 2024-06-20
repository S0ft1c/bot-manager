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

    # create a spam settings
    spam_settings = [InlineKeyboardButton(
        text='Настройки спам фильтров', callback_data='spam_settings_chat' + str(chatid))]

    # create a admin add remove
    admin_add_remove = [InlineKeyboardButton(
        text='Добавить/удалить админов', callback_data='admin_add_remove' + str(chatid))]

    # create a delete posts
    delete_posts = [InlineKeyboardButton(
        text='Удаление постов', callback_data='delete_posts' + str(chatid))]

    builder = InlineKeyboardMarkup(
        inline_keyboard=[
            rassilka,
            spam_settings,
            admin_add_remove,
            delete_posts,
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


async def spam_menu_kb(chat_id):
    builder = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Добавить спам слова',
                              callback_data='add_spam_w' + chat_id)],
        [InlineKeyboardButton(text='Убрать спам слова',
                              callback_data='remove_spam_w' + chat_id)],
        [InlineKeyboardButton(text='Изменить пересылку сообщений',
                              callback_data='peresilka_change' + chat_id)],
        [InlineKeyboardButton(text='Изаменить возможности ссылок',
                              callback_data='ssilka_change' + chat_id)],
        [InlineKeyboardButton(text='Настройка санкций',
                              callback_data='spam_ssankcii' + chat_id)],
        [InlineKeyboardButton(text='Настройка времени жизни сообщения',
                              callback_data='spam_time_life' + chat_id)]
    ])
    return builder


async def spam_sanctions(chat_id):
    chat = await db.get_chat_info_by_id(chat_id)
    sanction = chat.get('sanction', False)

    sss = [
        ['Предупреждение', 'warn'],
        ['Ограничение', 'mute'],
        ['Блокировка', 'ban'],
        ['Исключение', 'kick']
    ]

    builder = InlineKeyboardBuilder()
    for name in sss:
        if name[1] == sanction:
            builder.add(InlineKeyboardButton(
                text=name[0] + '!!!',
                callback_data='change_sanction' + name[1] + chat_id
            ))
        else:
            builder.add(InlineKeyboardButton(
                text=name[0],
                callback_data='change_sanction' + name[1] + chat_id
            ))
    return builder.adjust(1).as_markup()


async def admin_add_remove(admins, chat_id):
    builder = InlineKeyboardBuilder()

    for admin in admins:
        builder.add(InlineKeyboardButton(
            text=f'Удалить {admin.user.first_name}',
            callback_data='delete_admin' + str(admin.user.id) + str(chat_id)
        ))
    return builder.adjust(1).as_markup()
