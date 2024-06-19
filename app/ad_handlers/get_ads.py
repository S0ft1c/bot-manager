from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from mongo_db import db
import app.keyboards as kb
from utils import is_admin

router_get_ads = Router()


@router_get_ads.message(Command('get_ads'))
async def command_get_ads(message: Message):
    if not is_admin(message):
        logger.warning(
            f'Somebody (not an admin) tried to access the bot logic!!! His info -> {message.from_user}')
        return

    ads = await db.get_all_ads()

    await message.answer(
        text='Вот все ваши рекламные рассылки. Вы можете их просто удалить или отредактировать' +
        ' (просто заменить их на другое). Для удаления кнопка справа. Для редактирования нажмите на кнопку слева (время, на которое запланирована рассылка)',
        reply_markup=await kb.get_all_ads(ads)
    )
