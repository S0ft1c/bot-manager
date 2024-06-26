from utils import is_admin
from aiogram import Router, F
from aiogram.types import CallbackQuery
import app.keyboards as kb
from mongo_db import db
from loguru import logger

router_spam_sanctions = Router()


@router_spam_sanctions.callback_query(F.data.contains('spam_ssankcii'))
async def spam_ssankcii(callback: CallbackQuery):
    if not is_admin(callback):
        logger.warning(
            f'Somebody (not an admin) tried to access the bot logic!!! His info -> {callback.from_user}')
        return
    if callback.message.chat.type != 'private':
        return

    chat_id = callback.data.replace('spam_ssankcii', '')

    await callback.answer('')
    await callback.message.edit_text(
        text='Выберите санкции к спамеру!',
        reply_markup=await kb.spam_sanctions(chat_id)
    )


@router_spam_sanctions.callback_query(F.data.contains('change_sanction'))
async def change_sanction(callback: CallbackQuery):
    try:
        if not is_admin(callback):
            logger.warning(
                f'Somebody (not an admin) tried to access the bot logic!!! His info -> {callback.from_user}')
            return
        if callback.message.chat.type != 'private':
            return

        operation, chat_id = callback.data.replace(
            'change_sanction', '').split('-')
        chat_id = '-' + chat_id

        await db.update_sanction_in_chat(chat_id, operation)

        await callback.answer('')
        await callback.message.edit_text(
            text='Можно еще выбрать санкции...',
            reply_markup=await kb.spam_sanctions(chat_id)
        )
    except:  # best user fuck defense ever
        pass
