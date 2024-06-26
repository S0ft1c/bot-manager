from utils import is_admin
from aiogram import Router, F
from aiogram.types import CallbackQuery
from mongo_db import db
from loguru import logger
import app.keyboards as kb

router_peresilka_change = Router()


@router_peresilka_change.callback_query(F.data.contains('peresilka_change'))
async def peresilka_change(callback: CallbackQuery):
    if callback.message.chat.type != 'private':
        return
    if not is_admin(callback):
        logger.warning(
            f'Somebody (not an admin) tried to access the bot logic!!! His info -> {callback.from_user}')
        return

    chat_id = callback.data.replace('peresilka_change', '')
    await db.peresilka_change(chat_id)

    await callback.answer('')
    await callback.message.edit_text(text='Состояние пересылки изменено!',
                                     reply_markup=await kb.back_to_spam_settings_chat(chat_id))
