from aiogram import BaseMiddleware
from aiogram.types import Message
from loguru import logger
from typing import *
from mongo_db import db
from asyncio import sleep


class HiAndByeMiddleware(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        try:
            # if its left chat member
            if event.left_chat_member is not None and type(event) == Message and \
                    event.chat.type in ['group', 'supergroup']:

                bye_config = await db.get_bye_config(chat_id=event.chat.id)
                if bye_config.get('message', False):
                    ttt = bye_config['message'].replace(
                        '%username%', event.from_user.full_name)

                    result_message = await event.bot.send_message(
                        chat_id=event.chat.id,
                        text=ttt,
                        disable_notification=True
                    )
                    await sleep(bye_config.get('sleep_time', 5))
                    await result_message.delete()

        except Exception as e:
            pass
        return await handler(event, data)
