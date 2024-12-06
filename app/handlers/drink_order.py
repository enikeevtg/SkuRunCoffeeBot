from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram.utils.chat_action import ChatActionSender
import asyncio
import logging

from bot import bot, orders_spreadsheet
from database import requests as rq
from handlers import messages, start
from keyboards import categories_kb_builder, items_kb_builder
from keyboards import (drink_order_btn_text, back_to_categories_btn_cb,
                       confirm_btn_cb, reject_btn_cb, confirmation_kb)
from utils.facts import get_fact


router = Router(name=__name__)
logger = logging.getLogger(__name__)


class DrinkOrder(StatesGroup):
    order_in_process = State()
    order_done = State()


@router.message(F.text == drink_order_btn_text, StateFilter(None))
async def display_drink_categories(message: Message, state: FSMContext):
    logger.info(f'[{message.from_user.id}, {message.from_user.username}: ' + \
                f'{message.text}]')

    # Временная проверка наличия пользователя в базе данных
    nickname = await rq.get_nickname(message.from_user.id)
    if nickname == None:
        await start.cmd_start(message, state)
        return

    await message.answer(text=messages.choose_drink, 
                         reply_markup=await categories_kb_builder())
    await state.update_data(nickname=nickname)
    await state.set_state(DrinkOrder.order_in_process)


@router.message(F.text == drink_order_btn_text,
                StateFilter(DrinkOrder.order_in_process))
async def order_when_order_in_process(message: Message):
    logger.info(f'[{message.from_user.id}, {message.from_user.username}: ' + \
                f'{message.text}]')

    await message.answer(text=messages.choose_drink_above)


@router.message(F.text == drink_order_btn_text,
                StateFilter(DrinkOrder.order_done))
async def order_when_order_done(message: Message, state: FSMContext):
    logger.info(f'[{message.from_user.id}, {message.from_user.username}: ' + \
                f'{message.text}]')

    data = await state.get_data()
    name: str = data['nickname']
    drink: str = data['drink']
    await message.answer(messages.order_done.format(name, drink.lower()))


@router.callback_query(F.data.startswith('category_'))
async def display_drink_items_by_category(callback: CallbackQuery) -> None:
    logger.info(f'[{callback.from_user.id}, {callback.from_user.username}: ' + \
                f'{callback.data}]')

    await callback.answer()
    category_id = callback.data.split('_')[1]
    await callback.message.edit_text(text=messages.choose_option,
                              reply_markup=await items_kb_builder(category_id))


@router.callback_query(F.data == back_to_categories_btn_cb)
async def display_drink_categories_again(callback: CallbackQuery):
    logger.info(f'[{callback.from_user.id}, {callback.from_user.username}: ' + \
                f'{callback.data}]')
    
    await callback.answer(cache_time=11)
    await callback.message.edit_text(text=messages.choose_drink, 
                                     reply_markup=await categories_kb_builder())


@router.callback_query(F.data.startswith('item_'))
async def order_confirmation(callback: CallbackQuery,
                             state: FSMContext) -> None:
    logger.info(f'[{callback.from_user.id}, {callback.from_user.username}: ' + \
                f'{callback.data}]')

    await callback.answer()
    item = await rq.get_item_by_id(callback.data.split('_')[1])
    await state.update_data(drink=item.name)
    data = await state.get_data()
    await callback.message.edit_text(
                messages.order_confirmation
                        .format(data["nickname"], data["drink"]),
                reply_markup=confirmation_kb)


@router.callback_query(F.data == confirm_btn_cb, DrinkOrder.order_in_process)
async def create_order(callback: CallbackQuery, state: FSMContext):
    logger.info(f'[{callback.from_user.id}, {callback.from_user.username}: ' + \
                f'{callback.data}]')

    await callback.answer()
    data = await state.get_data()
    await callback.message.edit_text(text=messages.order_confirmed +
                                     str(data['drink']).lower())
    await state.set_state(DrinkOrder.order_done)
    await orders_spreadsheet.send_order(callback.from_user.id,
                                        callback.from_user.username,
                                        data['nickname'],
                                        data['drink'])
    async with ChatActionSender(bot=bot, chat_id=callback.from_user.id,
                                action='typing'):
        await asyncio.sleep(1)
        await callback.message.answer(await get_fact())


@router.callback_query(F.data == reject_btn_cb, DrinkOrder.order_in_process)
async def cancel_order(callback: CallbackQuery, state: FSMContext):
    logger.info(f'[{callback.from_user.id}, {callback.from_user.username}: ' + \
                f'{callback.data}]')

    await callback.answer()
    await callback.message.edit_text(text=messages.order_rejected)
    data = await state.get_data()
    await state.set_state(data.get('prev_state', None))
