from utils import is_admin
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
import datetime

router_un_user = Router()
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


@router_un_user.message(Command('un_user'))
async def mute_user(message: Message):
    if not is_admin(message):
        logger.warning(
            f'Somebody (not an admin) tried to access the bot logic!!! His info -> {message.from_user}')
        return
    if message.chat.type not in ['group', 'supergroup']:
        return

    if message.reply_to_message:
        man = message.reply_to_message.from_user.first_name
        member_to_unban = await message.chat.get_member(
            user_id=message.reply_to_message.from_user.id
        )
        if member_to_unban.status in ['left', 'banned']:
            await message.chat.unban(
                user_id=message.reply_to_message.from_user.id
            )
        await message.chat.restrict(
            user_id=message.reply_to_message.from_user.id,
            permissions=permissions
        )

        await message.answer(
            text=f'Пользователь {man} cнова в строю'
        )
    else:
        await message.answer(
            text='Выполните команду в ответ на сообщение пользователя, которого надо размутить'
        )
