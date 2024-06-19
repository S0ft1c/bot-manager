from utils import is_admin
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
import datetime

router_mute_user = Router()
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


@router_mute_user.message(Command('mute_user'))
async def mute_user(message: Message):
    if not is_admin(message):
        logger.warning(
            f'Somebody (not an admin) tried to access the bot logic!!! His info -> {message.from_user}')
        return
    if message.chat.type not in ['group', 'supergroup']:
        return

    if message.reply_to_message:
        man = message.reply_to_message.from_user.first_name
        await message.reply_to_message.chat.restrict(
            user_id=message.reply_to_message.from_user.id,
            permissions=restrictions,
            until_date=datetime.datetime.now() + datetime.timedelta(days=1)
        )
        await message.answer(
            text=f'Пользователь {man} замучен на 1 сутки'
        )
    else:
        await message.answer(
            text='Выполните команду в ответ на сообщение пользователя, которого надо замутить'
        )
