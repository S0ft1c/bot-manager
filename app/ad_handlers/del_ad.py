from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from mongo_db import db
from utils import is_admin

router_del_ad = Router()


@router_del_ad.callback_query(F.data.contains('del_ad'))
async def del_ad(callback: CallbackQuery):
    if not is_admin(callback):
        logger.warning(
            f'Somebody (not an admin) tried to access the bot logic!!! His info -> {message.from_user}')
        return

    ad_id = callback.data.replace('del_ad', '')
    await db.del_ad(ad_id)

    await callback.answer('')
    await callback.message.answer(text='Рекламная рассылка успешно удалена!')
