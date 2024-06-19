from aiogram import Router
from aiogram.types import Message
from utils import is_admin
from aiogram.filters import Command

router_ban_user = Router()


@router_ban_user.message(Command('ban_user'))
async def ban_user(message: Message):
    if not is_admin(message):
        logger.warning(
            f'Somebody (not an admin) tried to access the bot logic!!! His info -> {message.from_user}')
        return
    if message.chat.type not in ['group', 'supergroup']:
        return

    if message.reply_to_message:
        man = message.reply_to_message.from_user.first_name
        await message.chat.ban(
            user_id=message.reply_to_message.from_user.id
        )

        await message.answer(
            text=f'Пользователь {man} забанен'
        )
    else:
        await message.answer(
            text='Выполните команду в ответ на сообщение пользователя, которого надо забанить'
        )