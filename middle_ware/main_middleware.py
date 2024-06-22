from aiogram import BaseMiddleware
from aiogram.types import Message
from loguru import logger
from typing import *
from mongo_db import db


class MainMiddleware(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        try:
            if type(event) == Message and event.chat.type in ['group', 'supergroup']:
                msg = {
                    'message_id': event.message_id,
                    'user_id': event.from_user.id,
                    'chat_id': event.chat.id
                }
                await db.save_message(msg)
        except:
            pass

        return await handler(event, data)
