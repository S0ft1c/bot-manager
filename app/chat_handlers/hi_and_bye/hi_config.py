from aiogram import Router, F
from utils import is_admin
from aiogram.types import CallbackQuery, Message
from mongo_db import db
import app.keyboards as kb

router_hi_config = Router()


@router_hi_config.callback_query(F.data.contains('hi_config'))
async def hi_config(callback: CallbackQuery):
    chat_id = callback.data.replace('hi_config', '')
    hi_config = await db.get_hi_config(chat_id)

    match hi_config.get('type', False):
        case False:
            text = 'Выберите тип приветственного сообщения!'
            await callback.message.answer(
                text=text,
                reply_markup=await kb.new_hi_config(chat_id)
            )
        case 'pereliv':
            text = f'Указанные каналы для перелива = {len(hi_config.get('channels', []))}\n' + \
                f'Время до удаления сообщения = {
                    hi_config.get('sleep_time', 5)}'

            await callback.message.answer(
                text=text,
                reply_markup=await kb.hi_config_pereliv(chat_id)
            )
        case 'priglasit':
            text = f'Количество людей, которое надо пригласить = {hi_config.get('members_came', 1)}\n' + \
                f'Время до удаления сообщения = {
                    hi_config.get('sleep_time', 5)}'

            await callback.message.answer(
                text=text,
                reply_markup=await kb.hi_config_priglasit(chat_id)
            )

        case 'combined':
            text = f'Указанные каналы для перелива = {len(hi_config.get('channels', []))}\n' + \
                f'Количество людей, которое надо пригласить = {hi_config.get('members_came', 1)}\n' + \
                f'Время до удаления сообщения = {
                    hi_config.get('sleep_time', 5)}'

            await callback.message.answer(
                text=text,
                reply_markup=await kb.hi_config_combined(chat_id)
            )

    await callback.answer('')


@router_hi_config.callback_query(F.data.contains('hi_type_pereliv'))
async def hi_type_pereliv(callback: CallbackQuery):
    chat_id = callback.data.replace('hi_type_pereliv', '')
    await db.create_new_hi_config(chat_id, 'pereliv')

    hi_config = await db.get_hi_config(chat_id)

    match hi_config.get('type', False):
        case False:
            text = 'Выберите тип приветственного сообщения!'
            await callback.message.answer(
                text=text,
                reply_markup=await kb.new_hi_config(chat_id)
            )
        case 'pereliv':
            text = f'Указанные каналы для перелива = {len(hi_config.get('channels', []))}\n' + \
                f'Время до удаления сообщения = {
                    hi_config.get('sleep_time', 5)}'

            await callback.message.answer(
                text=text,
                reply_markup=await kb.hi_config_pereliv(chat_id)
            )
        case 'priglasit':
            text = f'Количество людей, которое надо пригласить = {hi_config.get('members_came', 1)}\n' + \
                f'Время до удаления сообщения = {
                    hi_config.get('sleep_time', 5)}'

            await callback.message.answer(
                text=text,
                reply_markup=await kb.hi_config_priglasit(chat_id)
            )

        case 'combined':
            text = f'Указанные каналы для перелива = {len(hi_config.get('channels', []))}\n' + \
                f'Количество людей, которое надо пригласить = {hi_config.get('members_came', 1)}' + \
                f'Время до удаления сообщения = {
                    hi_config.get('sleep_time', 5)}'

            await callback.message.answer(
                text=text,
                reply_markup=await kb.hi_config_combined(chat_id)
            )

    await callback.answer('')


@router_hi_config.callback_query(F.data.contains('hi_type_priglasit'))
async def hi_type_priglasit(callback: CallbackQuery):
    chat_id = callback.data.replace('hi_type_priglasit', '')
    await db.create_new_hi_config(chat_id, 'priglasit')

    hi_config = await db.get_hi_config(chat_id)

    match hi_config.get('type', False):
        case False:
            text = 'Выберите тип приветственного сообщения!'
            await callback.message.answer(
                text=text,
                reply_markup=await kb.new_hi_config(chat_id)
            )
        case 'pereliv':
            text = f'Указанные каналы для перелива = {len(hi_config.get('channels', []))}\n' + \
                f'Время до удаления сообщения = {
                    hi_config.get('sleep_time', 5)}'

            await callback.message.answer(
                text=text,
                reply_markup=await kb.hi_config_pereliv(chat_id)
            )
        case 'priglasit':
            text = f'Количество людей, которое надо пригласить = {hi_config.get('members_came', 1)}' + \
                f'Время до удаления сообщения = {
                    hi_config.get('sleep_time', 5)}'

            await callback.message.answer(
                text=text,
                reply_markup=await kb.hi_config_priglasit(chat_id)
            )

        case 'combined':
            text = f'Указанные каналы для перелива = {len(hi_config.get('channels', []))}\n' + \
                f'Количество людей, которое надо пригласить = {hi_config.get('members_came', 1)}' + \
                f'Время до удаления сообщения = {
                    hi_config.get('sleep_time', 5)}'

            await callback.message.answer(
                text=text,
                reply_markup=await kb.hi_config_combined(chat_id)
            )

    await callback.answer('')


@router_hi_config.callback_query(F.data.contains('hi_type_combined'))
async def hi_type_combined(callback: CallbackQuery):
    chat_id = callback.data.replace('hi_type_combined', '')
    await db.create_new_hi_config(chat_id, 'combined')

    hi_config = await db.get_hi_config(chat_id)

    match hi_config.get('type', False):
        case False:
            text = 'Выберите тип приветственного сообщения!'
            await callback.message.answer(
                text=text,
                reply_markup=await kb.new_hi_config(chat_id)
            )
        case 'pereliv':
            text = f'Указанные каналы для перелива = {len(hi_config.get('channels', []))}\n' + \
                f'Время до удаления сообщения = {
                    hi_config.get('sleep_time', 5)}'

            await callback.message.answer(
                text=text,
                reply_markup=await kb.hi_config_pereliv(chat_id)
            )
        case 'priglasit':
            text = f'Количество людей, которое надо пригласить = {hi_config.get('members_came', 1)}\n' + \
                f'Время до удаления сообщения = {
                    hi_config.get('sleep_time', 5)}'

            await callback.message.answer(
                text=text,
                reply_markup=await kb.hi_config_priglasit(chat_id)
            )

        case 'combined':
            text = f'Указанные каналы для перелива = {len(hi_config.get('channels', []))}\n' + \
                f'Количество людей, которое надо пригласить = {hi_config.get('members_came', 1)}\n' + \
                f'Время до удаления сообщения = {
                    hi_config.get('sleep_time', 5)}'

            await callback.message.answer(
                text=text,
                reply_markup=await kb.hi_config_combined(chat_id)
            )

    await callback.answer('')


@router_hi_config.callback_query(F.data.contains('new_hi_confiig'))
async def new_hi_confiig(callback: CallbackQuery):
    chat_id = callback.data.replace('new_hi_confiig', '')
    await db.erase_hi_config(chat_id)

    hi_config = await db.get_hi_config(chat_id)

    match hi_config.get('type', False):
        case False:
            text = 'Выберите тип приветственного сообщения!'
            await callback.message.answer(
                text=text,
                reply_markup=await kb.new_hi_config(chat_id)
            )
        case 'pereliv':
            text = f'Указанные каналы для перелива = {len(hi_config.get('channels', []))}\n' + \
                f'Время до удаления сообщения = {
                    hi_config.get('sleep_time', 5)}'

            await callback.message.answer(
                text=text,
                reply_markup=await kb.hi_config_pereliv(chat_id)
            )
        case 'priglasit':
            text = f'Количество людей, которое надо пригласить = {hi_config.get('members_came', 1)}\n' + \
                f'Время до удаления сообщения = {
                    hi_config.get('sleep_time', 5)}'

            await callback.message.answer(
                text=text,
                reply_markup=await kb.hi_config_priglasit(chat_id)
            )

        case 'combined':
            text = f'Указанные каналы для перелива = {len(hi_config.get('channels', []))}\n' + \
                f'Количество людей, которое надо пригласить = {hi_config.get('members_came', 1)}\n' + \
                f'Время до удаления сообщения = {
                    hi_config.get('sleep_time', 5)}'

            await callback.message.answer(
                text=text,
                reply_markup=await kb.hi_config_combined(chat_id)
            )

    await callback.answer('')
