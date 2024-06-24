from aiogram import Router, F
from utils import is_admin
from aiogram.types import CallbackQuery, Message
import app.keyboards as kb

router_hi_and_bye_menu = Router()


@router_hi_and_bye_menu.callback_query(F.data.contains('hi_and_bye_menu'))
async def hi_and_bye_menu(callback: CallbackQuery):
    chat_id = callback.data.replace('hi_and_bye_menu', '')

    await callback.answer('')
    await callback.message.answer(
        text='Выберите, что вы хотите настроить!',
        reply_markup=await kb.hi_and_buy_menu(chat_id)
    )
