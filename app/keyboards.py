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

    # create a hi and bye
    hi_and_bye = [InlineKeyboardButton(text='Приветствия и прощания',
                                       callback_data='hi_and_bye_menu' + str(chatid))]

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

    # create the text config file
    text_conf = [InlineKeyboardButton(
        text='Настройка сообщений бота действия в чате.', callback_data='text_conf' + str(chatid))]

    # create a delete posts
    delete_posts = [InlineKeyboardButton(
        text='Удаление постов', callback_data='delete_posts' + str(chatid))]

    # create reputation system
    rep_system = [InlineKeyboardButton(
        text='Система репутации', callback_data='rep_sys_inf' + str(chatid))]

    # create for the restrict all
    restrict_all = [InlineKeyboardButton(
        text='Возможность писать сообщения (всем)', callback_data='restrict_all_inf' + str(chatid))]

    builder = InlineKeyboardMarkup(
        inline_keyboard=[
            hi_and_bye,
            rassilka,
            spam_settings,
            admin_add_remove,
            text_conf,
            delete_posts,
            rep_system,
            restrict_all
        ],
    )
    return builder


async def restrict_all_kb(chat_id):
    builder = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text='Запретить всем отправлять сообщения', callback_data='restrict_all_on' + str(chat_id))],
        [InlineKeyboardButton(
            text='Разрешить всем отправлять сообщения', callback_data='restrict_all_off' + str(chat_id))],
    ])
    return builder


async def rep_sys_info(chat_id):
    builder = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Изменить состояние системы репутации',
                              callback_data='rep_sys_change' + str(chat_id))],
        [InlineKeyboardButton(text='Добавить слова репутации',
                              callback_data='rep_w_add' + str(chat_id))],
        [InlineKeyboardButton(text='Убрать слова репутации',
                              callback_data='rep_w_remove' + str(chat_id))]
    ])
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


async def text_conf_kb(chat_id):
    builder = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Предупреждение /warn',
                              callback_data='text_change_warn' + str(chat_id))],
        [InlineKeyboardButton(text='Ограничение на отправку сообщений /mute',
                              callback_data='text_change_mute' + str(chat_id))],
        [InlineKeyboardButton(text='Блокировка /ban',
                              callback_data='text_change_ban' + str(chat_id))],
        [InlineKeyboardButton(text='Исключение /kick',
                              callback_data='text_change_kick' + str(chat_id))],
        [InlineKeyboardButton(text='Снятие ограничеий /un',
                              callback_data='text_change_un' + str(chat_id))],
    ])
    return builder


async def hi_and_buy_menu(chat_id):
    builder = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Приветственное сообщение',
                              callback_data='hi_config' + str(chat_id))],
        [InlineKeyboardButton(text='Прощальное сообщение',
                              callback_data='bye_config' + str(chat_id))],
    ])
    return builder


async def bye_menu(chat_id):
    builder = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Изменить сообщение',
                              callback_data='bye_message_change' + str(chat_id))],
        [InlineKeyboardButton(text='Изменить время до удаления',
                              callback_data='bye_time_change' + str(chat_id))]
    ])
    return builder


async def new_hi_config(chat_id):
    builder = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Перелив в другие каналы',
                              callback_data='hi_type_pereliv' + str(chat_id))],
        [InlineKeyboardButton(text='Пригласить определенное количество людей',
                              callback_data='hi_type_priglasit' + str(chat_id))],
        [InlineKeyboardButton(text='Использовать и то и другое',
                              callback_data='hi_type_combined' + str(chat_id))]
    ])
    return builder


async def hi_config_pereliv(chat_id):
    builder = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Добавить каналы',
                              callback_data='hi_pereliv_chanells_menu' + str(chat_id))],
        [InlineKeyboardButton(text='Изменить сообщение',
                              callback_data='hi_message_change' + str(chat_id))],
        [InlineKeyboardButton(text='Изменить время до удаления',
                              callback_data='hi_time_change' + str(chat_id))],
        [InlineKeyboardButton(text='Поменять конфигурацию (ВСЕ УДАЛИТСЯ)',
                              callback_data='new_hi_confiig' + str(chat_id))]
    ])
    return builder


async def hi_config_priglasit(chat_id):
    builder = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Изменить количество людей',
                              callback_data='hi_members_came_change' + str(chat_id))],
        [InlineKeyboardButton(text='Изменить сообщение',
                              callback_data='hi_message_change' + str(chat_id))],
        [InlineKeyboardButton(text='Изменить время до удаления',
                              callback_data='hi_time_change' + str(chat_id))],
        [InlineKeyboardButton(text='Поменять конфигурацию (ВСЕ УДАЛИТСЯ)',
                              callback_data='new_hi_confiig' + str(chat_id))]
    ])
    return builder


async def hi_config_combined(chat_id):
    builder = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Добавить каналы',
                              callback_data='hi_pereliv_chanells_menu' + str(chat_id))],
        [InlineKeyboardButton(text='Изменить количество людей',
                              callback_data='hi_members_came_change' + str(chat_id))],
        [InlineKeyboardButton(text='Изменить сообщение',
                              callback_data='hi_message_change' + str(chat_id))],
        [InlineKeyboardButton(text='Изменить время до удаления',
                              callback_data='hi_time_change' + str(chat_id))],
        [InlineKeyboardButton(text='Поменять конфигурацию (ВСЕ УДАЛИТСЯ)',
                              callback_data='new_hi_confiig' + str(chat_id))]
    ])
    return builder


async def hi_pereliv_chanells(channels):
    builder = InlineKeyboardBuilder()
    for el in channels:
        builder.add(InlineKeyboardButton(text=f'УДАЛИТЬ {el}',
                                         callback_data='hi_del_channel' + el))
    return builder.adjust(1).as_markup()


async def welcome_message_pereliv(channels):
    builder = InlineKeyboardBuilder()
    for el in channels:
        builder.add(InlineKeyboardButton(text=f'Подпишись',
                                         url=el.invite_link))
    return builder.adjust(1).as_markup()


async def start_kbkkbkb(link):
    builder = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Вот наша группа', url=link.invite_link)]
    ])
    return builder
