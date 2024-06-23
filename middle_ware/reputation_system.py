from aiogram import BaseMiddleware
from aiogram.types import Message
from loguru import logger
from typing import *
from mongo_db import db


class ReputationSystem(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        try:
            rep_sys_workin = await db.get_rep_sys_workin(event.chat.id)
            if rep_sys_workin and type(event) == Message and event.chat.type in ['group', 'supergroup'] and \
                    event.reply_to_message:
                chat_id = event.chat.id
                user_id = event.from_user.id

                words = event.text.lower().split()
                reputation_w = await db.get_reputation_w(chat_id)
                if set(words) & set(reputation_w):
                    await db.add_rep_to_user(chat_id, user_id)

        except:
            pass
        return await handler(event, data)
