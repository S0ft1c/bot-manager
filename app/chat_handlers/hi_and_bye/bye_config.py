from aiogram import Router, F
from utils import is_admin
from aiogram.types import CallbackQuery, Message
from mongo_db import db
import app.keyboards as kb

router_bye_config = Router()


@router_bye_config.callback_query(F.data.contains('bye_config'))
async def bye_config(callback: CallbackQuery):
    chat_id = callback.data.replace('bye_config', '')
    bye_config = await db.get_bye_config(chat_id)

    current_message = bye_config.get('message', 'тут пусто...')
    sleep_time = bye_config.get('sleep_time', 5)

    text = f'Текущий текст прощального сообщения:\n{current_message}\n' + \
        f'\nВремя до удаления сообщения = {sleep_time}'

    await callback.answer('')
    await callback.message.edit_text(
        text=text,
        reply_markup=await kb.bye_menu(chat_id)
    )
