from aiogram import Router, F
from aiogram.types import CallbackQuery
from mongo_db import db
import app.keyboards as kb
from utils import is_admin
from loguru import logger

router_spam_settings_menu = Router()


@router_spam_settings_menu.callback_query(F.data.contains('spam_settings_chat'))
async def spam_settings_menu(callback: CallbackQuery):
    if not is_admin(callback):
        logger.warning(
            f'Somebody (not an admin) tried to access the bot logic!!! His info -> {callback.from_user}')
        return
    if callback.message.chat.type != 'private':
        return

    # chat data get
    chat_id = callback.data.replace('spam_settings_chat', '')
    chat_info = await db.get_chat_info_by_id(chat_id)
    spam_w = chat_info.get("spam_w", "Никаких")
    if spam_w != 'Никаких':
        spam_w = ';'.join(spam_w)
    peresilka = 'Включен' if chat_info.get(
        'peresilka', False) else 'Отсутствует'
    ssilki = 'Да' if chat_info.get('ssilka', True) else 'Нет'

    text = f'<b>Группа:</b> {chat_info["title"]}\n<b>Спам слова:</b> {spam_w}\n' + \
        f'<b>Запрет пересылающихся сообщений:</b> {peresilka}\n' + \
        f'<b>Ссылки разрешены:</b> {ssilki}'

    await callback.answer('')
    await callback.message.edit_text(
        text=text,
        reply_markup=await kb.spam_menu_kb(chat_id),
        parse_mode='HTML'
    )
