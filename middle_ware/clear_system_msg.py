from aiogram import BaseMiddleware
from aiogram.types import Message
from loguru import logger
from typing import *
from mongo_db import db


class ClearSystem(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        try:
            if type(event) == Message and event.chat.type in ['group', 'supergroup']:

                sss = [
                    event.new_chat_members, event.left_chat_member,
                    event.new_chat_title, event.new_chat_photo, event.delete_chat_photo, event.group_chat_created,
                    event.supergroup_chat_created,
                    event.pinned_message
                ]

                system_notification = [
                    1 if el is not None else 0
                    for el in sss
                ]
                if sum(system_notification) != 0:
                    logger.warning('System notification')
                    await event.delete()
        except Exception as e:
            pass

        return await handler(event, data)
