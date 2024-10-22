from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
import logging

from handlers import drinks
from database import requests as rq
from handlers import messages, start
from keyboards import (categories_kb_builder, items_kb_builder,
                       confirmation_kb_builder)
from utils import gsheets


router = Router()
logger = logging.getLogger(__name__)


# FSM states
class DrinkOrder(StatesGroup):
    order_in_process = State()
    order_done = State()


@router.message(Command('menu'), StateFilter(None))
async def cmd_menu(message: Message, state: FSMContext):
    logger.info(f'[{message.from_user.id}, {message.from_user.username}: ' + \
                f'{message.text}]')

    # Временная проверка наличия пользователя в базе данных
    cup_name = await rq.get_user_cup_name(message.from_user.id)
    if cup_name == None:
        await start.cmd_start(message, state)
        return

    await message.answer(text=messages.choose_drink, 
                         reply_markup=await categories_kb_builder())
    await state.update_data(name=cup_name)
    await state.set_state(DrinkOrder.order_in_process) 


@router.message(Command('menu'), StateFilter(DrinkOrder.order_done))
async def cmd_menu(message: Message, state: FSMContext):
    logger.info(f'[{message.from_user.id}, {message.from_user.username}: ' + \
                f'{message.text}]')

    data = await state.get_data()
    name: str = data['name']
    drink: str = data['drink']
    await message.answer(messages.order_done.format(name, drink.lower()))


@router.callback_query(F.data.startswith('category_'))
async def drink_items_by_category(callback: CallbackQuery) -> None:
    logger.info(f'[{callback.from_user.id}, {callback.from_user.username}: ' + \
                f'{callback.data}]')

    await callback.answer()
    category_id = callback.data.split('_')[1]
    await callback.message.edit_text(text=messages.choose_option,
                              reply_markup=await items_kb_builder(category_id))


@router.callback_query(F.data.startswith('item_'))
async def order_confirmation(callback: CallbackQuery,
                             state: FSMContext) -> None:
    logger.info(f'[{callback.from_user.id}, {callback.from_user.username}: ' + \
                f'{callback.data}]')

    item = await rq.get_item_by_id(callback.data.split('_')[1])
    drink = item.name
    await state.update_data(drink=drink)
    data = await state.get_data()
    await callback.message.edit_text(
        f'Твой заказ:\n{data["name"]} — {data["drink"]}\nВсё верно?',
        reply_markup=await confirmation_kb_builder())


@router.callback_query(F.data == 'confirm', DrinkOrder.order_in_process)
async def create_order(callback: CallbackQuery, state: FSMContext):
    logger.info(f'[{callback.from_user.id}, {callback.from_user.username}: ' + \
                f'{callback.data}]')

    data = await state.get_data()
    await callback.message.edit_text(text=messages.success_order_msg +
                                     str(data['drink']).lower())
    await callback.answer('')
    await state.set_state(DrinkOrder.order_done)
    gsheets.send_order_to_google_sheet(data['name'], data['drink'])


@router.callback_query(F.data == 'reject', DrinkOrder.order_in_process)
async def cancel_order(callback: CallbackQuery, state: FSMContext):
    logger.info(f'[{callback.from_user.id}, {callback.from_user.username}: ' + \
                f'{callback.data}]')

    await callback.message.edit_text(text='Окей, давай начнём сначала! ' +
                                     messages.commands)
    await callback.answer('')
    await state.clear()
