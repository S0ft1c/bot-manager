from utils import is_admin
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from loguru import logger
import app.keyboards as kb
from mongo_db import db

router_restrict_all = Router()
restrictions = {
    'can_send_messages': False,
    'can_send_audios': False,
    'can_send_documents': False,
    'can_send_documents': False,
    'can_send_documents': False,
    'can_send_video_notes': False,
    'can_send_voice_notes': False,
    'can_send_polls': False,
    'can_send_other_messages': False,
}
permissions = {
    'can_send_messages': True,
    'can_send_audios': True,
    'can_send_documents': True,
    'can_send_documents': True,
    'can_send_documents': True,
    'can_send_video_notes': True,
    'can_send_voice_notes': True,
    'can_send_polls': True,
    'can_send_other_messages': True,
}


@router_restrict_all.callback_query(F.data.contains('restrict_all_inf'))
async def restrict_all_inf(callback: CallbackQuery):
    if not is_admin(callback):
        logger.warning(
            f'Somebody (not an admin) tried to access the bot logic!!! His info -> {callback.message.from_user.id}')
        return
    if callback.message.chat.type != 'private':
        return

    chat_id = callback.data.replace('restrict_all_inf', '')

    await callback.answer('')
    await callback.message.edit_text(
        text='Выберите действие',
        reply_markup=await kb.restrict_all_kb(chat_id),
    )


@router_restrict_all.callback_query(F.data.contains('restrict_all_on'))
async def restrict_all_on(callback: CallbackQuery):
    if not is_admin(callback):
        logger.warning(
            f'Somebody (not an admin) tried to access the bot logic!!! His info -> {callback.message.from_user.id}')
        return
    if callback.message.chat.type != 'private':
        return

    chat_id = callback.data.replace('restrict_all_on', '')
    msgs = await db.get_all_messages_from_chat(chat_id)

    members = set(msg['user_id'] for msg in msgs)
    for member in members:
        try:
            await callback.message.bot.restrict_chat_member(
                chat_id=int(chat_id),
                user_id=int(member),
                permissions=restrictions
            )
        except Exception as e:
            logger.warning(e)

    await callback.answer('')
    await callback.message.edit_text(
        text='Никто теперь не будет писать в эту группу!',
        reply_markup=await kb.back_to_spam_settings_chat(chat_id)
    )


@router_restrict_all.callback_query(F.data.contains('restrict_all_off'))
async def restrict_all_on(callback: CallbackQuery):
    if not is_admin(callback):
        logger.warning(
            f'Somebody (not an admin) tried to access the bot logic!!! His info -> {callback.message.from_user.id}')
        return
    if callback.message.chat.type != 'private':
        return

    chat_id = callback.data.replace('restrict_all_off', '')
    msgs = await db.get_all_messages_from_chat(chat_id)

    members = set(msg['user_id'] for msg in msgs)
    for member in members:
        try:
            await callback.message.bot.restrict_chat_member(
                chat_id=int(chat_id),
                user_id=int(member),
                permissions=permissions
            )
        except Exception as e:
            logger.warning(e)

    await callback.answer('')
    await callback.message.edit_text(
        text='Теперь все могут писать в эту группу!',
        reply_markup=await kb.back_to_spam_settings_chat(chat_id)
    )
