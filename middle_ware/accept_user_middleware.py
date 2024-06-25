from aiogram import BaseMiddleware
from aiogram.types import Message
from loguru import logger
from utils import is_admin
from typing import *
from mongo_db import db
from asyncio import sleep
import app.keyboards as kb
from aiogram.utils.deep_linking import create_start_link


class AcceptMessageMiddleware(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        if is_admin(event):
            return await handler(event, data)

        if type(event) == Message and event.chat.type in ['group', 'supergroup']:
            hi_config = await db.get_hi_config(event.chat.id)
            match hi_config.get('type', False):
                case False:
                    return await handler(event, data)
                case 'pereliv':
                    g = True
                    for el in hi_config.get('channels', []):
                        user_status = await event.bot.get_chat_member(chat_id=el, user_id=event.from_user.id)
                        if user_status.status in ['left', 'banned']:
                            g = False
                            break
                    if g:
                        return await handler(event, data)
                    else:
                        await shit(event)
                        await event.delete()
                case 'priglasit':
                    members_cnt = await db.get_came_users(event.chat.id, event.from_user.id)
                    members_cnt = set(members_cnt) - 1

                    if members_cnt >= hi_config.get('members_came', 5):
                        return await handler(event, data)
                    else:
                        await shit(event)
                        await event.delete()
                case 'combined':
                    g = True
                    for el in hi_config.get('channels', []):
                        user_status = await event.bot.get_chat_member(chat_id=el, user_id=event.from_user.id)
                        if user_status.status in ['left', 'banned']:
                            g = False
                            break
                    if not g:
                        await shit(event)
                        await event.delete()

                    members_cnt = await db.get_came_users(event.chat.id, event.from_user.id)
                    members_cnt = set(members_cnt) - 1

                    logger.info(f'member_came = {members_cnt}')
                    if members_cnt >= hi_config.get('members_came', 5):
                        return await handler(event, data)
                    else:
                        await shit(event)
                        await event.delete()
        else:
            return await handler(event, data)


async def shit(event: Message):
    hi_config = await db.get_hi_config(event.chat.id)
    match hi_config.get('type', False):
        case False:
            pass
        case 'pereliv':
            message = hi_config.get('message')
            channels = hi_config.get('channels')
            lll = [await event.bot.create_chat_invite_link(chat_id=el) for el in channels]
            sleep_time = hi_config.get('sleep_time', 5)
            kkb = await kb.welcome_message_pereliv(lll)
            result_msg = await event.bot.send_message(
                chat_id=event.chat.id,
                text=message,
                reply_markup=kkb,
            )
            await sleep(sleep_time)
            await result_msg.delete()
        case 'priglasit':
            link = await create_start_link(event.bot, f'{event.chat.id}00000{event.from_user.id}', False)
            # link = f'https://t.me/stephans_programming_test_bot?start={
            #     event.chat.id}|{event.from_user.id}'
            members_came = hi_config.get(members_came)
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
            members_came = hi_config.get('members_came')
            message = hi_config.get('message')
            message += (f'\nТвоя ссылка для приглашения -> {link}\n' +
                        f'Тебе надо пригласить {members_came}.')

            channels = hi_config.get('channels')
            lll = [await event.bot.create_chat_invite_link(chat_id=el) for el in channels]
            sleep_time = hi_config.get('sleep_time')
            kkb = await kb.welcome_message_pereliv(lll)
            result_msg = await event.bot.send_message(
                chat_id=event.chat.id,
                text=message,
                reply_markup=kkb
            )
            await sleep(sleep_time)
            await result_msg.delete()
