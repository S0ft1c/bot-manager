from utils import is_admin
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from mongo_db import db

router_top_rating = Router()


@router_top_rating.message(Command('top_rating'))
async def top_rating(message: Message):
    if message.chat.type not in ['group', 'supergroup']:
        return

    chat_id = message.chat.id
    user_rep = await db.get_user_rep(chat_id)
    user_rep = sorted(user_rep.items(), key=lambda x: (-x[-1]))[:10]

    mmm = []
    for user_str_id, reputation in user_rep:
        member = await message.bot.get_chat_member(
            chat_id=chat_id,
            user_id=int(user_str_id)
        )
        mmm.append(
            f'{member.user.full_name} = {reputation} репутации'
        )
    text = '\n'.join(mmm)

    await message.answer(
        text=text
    )
