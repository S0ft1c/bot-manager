from aiogram import BaseMiddleware
from aiogram.types import Message
from loguru import logger
from typing import *
from mongo_db import db
import datetime


restrictions = {
    'can_send_messages': False,
    'can_send_audios': False,
    'can_send_documents': False,
    'can_send_documents': False,
    'can_send_documents': False,
    'can_send_video_notes': False,
    'can_send_voice_notes': False,
    'can_send_polls': False,
    'can_send_other_messages': False,
}
permissions = {
    'can_send_messages': True,
    'can_send_audios': True,
    'can_send_documents': True,
    'can_send_documents': True,
    'can_send_documents': True,
    'can_send_video_notes': True,
    'can_send_voice_notes': True,
    'can_send_polls': True,
    'can_send_other_messages': True
}


class AntispamMiddleware(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        try:
            if type(event) == Message and event.chat.type in ['group', 'supergroup']:
                words = set(event.text.split())
                chat_id = event.chat.id
                spam_w = await db.get_spam_w(chat_id)
                restrict_peresilka = await db.get_peresilka(chat_id)
                ssilki_allowed = await db.get_ssilka(chat_id)

                arr = [] if event.entities is None else [
                    el for el in event.entities if el.type == 'text_link']
                if (set(words) & set(spam_w)) or ((event.forward_sender_name is not None) and restrict_peresilka) \
                        or ((not ssilki_allowed) and ('http' in event.text or arr)):
                    logger.warning('FINDED SPAM')
                    user_id = event.from_user.id

                    # spam policy
                    spam_policy = await db.get_sanction(chat_id)

                    # switches
                    match spam_policy:
                        case 'warn':
                            await db.add_warn_to_user(user_id)
                        case 'mute':
                            await event.bot.restrict_chat_member(
                                chat_id=chat_id, user_id=user_id,
                                permissions=restrictions,
                                until_date=datetime.datetime.now() + datetime.timedelta(days=1)
                            )
                        case 'ban':
                            await event.chat.ban(user_id)
                        case 'kick':
                            await event.chat.ban(
                                user_id=user_id
                            )
                            member_to_unban = await event.chat.get_member(
                                user_id=user_id
                            )
                            if member_to_unban.status in ['left', 'banned']:
                                await event.chat.unban(
                                    user_id=user_id
                                )
                            await event.chat.restrict(
                                user_id=user_id,
                                permissions=permissions
                            )
                    await event.delete()
                    return
        except Exception as e:
            logger.error(e)
        return await handler(event, data)
