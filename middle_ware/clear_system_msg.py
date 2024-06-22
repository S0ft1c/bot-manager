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
        if type(event) == Message and event.chat.type in ['group', 'supergroup']:
            print(event)
        return await handler(event, data)
