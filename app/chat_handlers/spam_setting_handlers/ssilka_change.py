from utils import is_admin
from aiogram import Router, F
from aiogram.types import CallbackQuery
from mongo_db import db
from loguru import logger
import app.keyboards as kb

router_ssilka_change = Router()


@router_ssilka_change.callback_query(F.data.contains('ssilka_change'))
async def ssilka_change(callback: CallbackQuery):
    if not is_admin(callback):
        logger.warning(
            f'Somebody (not an admin) tried to access the bot logic!!! His info -> {callback.from_user}')
        return
    if callback.message.chat.type != 'private':
        return

    chat_id = callback.data.replace('ssilka_change', '')
    await db.ssilka_change(chat_id)

    await callback.answer('')
    await callback.message.edit_text(text='Состояние ссылок изменено!',
                                     reply_markup=await kb.back_to_spam_settings_chat(chat_id))
