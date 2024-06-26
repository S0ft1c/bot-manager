from aiogram import BaseMiddleware
from aiogram.types import Message
from loguru import logger
from typing import *
from mongo_db import db
from asyncio import sleep
import app.keyboards as kb
from aiogram.utils.deep_linking import create_start_link


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
                    return await handler(event, data)

            # if its new chat member
            elif event.new_chat_members is not None and type(event) == Message and \
                    event.chat.type in ['group', 'supergroup']:

                hi_config = await db.get_hi_config(event.chat.id)
                match hi_config.get('type', False):
                    case False:
                        pass
                    case 'pereliv':
                        message = hi_config.get('message')
                        channels = hi_config.get('channels')
                        sleep_time = hi_config.get('sleep_time')
                        kkb = await kb.welcome_message_pereliv(channels)
                        result_msg = await event.bot.send_message(
                            text=message,
                            reply_markup=kkb,
                            chat_id=event.chat.id
                        )
                        await sleep(sleep_time)
                        await result_msg.delete()
                        return await handler(event, data)

                    case 'priglasit':
                        # link = f'https://t.me/stephans_programming_test_bot?start={
                        #     event.chat.id}|{event.from_user.id}'
                        # members_came = len(hi_config.get('members_came')) - 1
                        # sleep_time = hi_config.get('sleep_time')
                        # message = hi_config.get('message')
                        # message += (f'\nТвоя ссылка для приглашения -> {link}\n' +
                        #             f'Тебе надо пригласить {members_came}.')
                        # result_msg = await event.bot.send_message(
                        #     text=message,
                        #     chat_id=event.chat.id
                        # )
                        # await sleep(sleep_time)
                        # await result_msg.delete()
                        # return await handler(event, data)
                        link = await create_start_link(event.bot, f'{event.chat.id}00000{event.from_user.id}', False)
                        # link = f'https://t.me/stephans_programming_test_bot?start={
                        #     event.chat.id}|{event.from_user.id}'
                        members_came = hi_config.get('members_came')
                        sleep_time = hi_config.get('sleep_time')
                        message = hi_config.get('message')
                        message += (f'\nТвоя ссылка для приглашения -> {link}\n' +
                                    f'Тебе надо пригласить {members_came}.')
                        result_msg = await event.bot.send_message(
                            chat_id=event.chat.id,
                            text=message,
                        )
                        await sleep(sleep_time)
                        await result_msg.delete()

                    case 'combined':
                        message = hi_config.get('message')

                        link = await create_start_link(event.bot, f'{event.chat.id}00000{event.from_user.id}', False)
                        members_came = len(hi_config.get(members_came)) - 1
                        message = hi_config.get('message')
                        message += (f'\nТвоя ссылка для приглашения -> {link}\n' +
                                    f'Тебе надо пригласить {members_came}.')

                        channels = hi_config.get('channels')
                        sleep_time = hi_config.get('sleep_time')
                        kkb = await kb.welcome_message_pereliv(channels)
                        result_msg = await event.bot.send_message(
                            text=message,
                            reply_markup=kkb,
                            chat_id=event.chat.id
                        )
                        await sleep(sleep_time)
                        await result_msg.delete()
                        return await handler(event, data)

        except Exception as e:
            logger.error(e)
        return await handler(event, data)
