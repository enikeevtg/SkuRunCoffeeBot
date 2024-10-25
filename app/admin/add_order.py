# Добавление заказа вручную админом

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message
import logging

from handlers.drink_order import DrinkOrder
from utils import gsheets
from keyboards import add_order_btn_cb, admins_kb


router = Router()
logger = logging.getLogger(__name__)


class AdminDrinkOrder(StatesGroup):
    set_nickname = State()
    set_drink = State()
    order_done = State()


@router.callback_query(F.data == add_order_btn_cb,
                       StateFilter(None, DrinkOrder.order_done))
async def add_order(callback: CallbackQuery, state: FSMContext):
    logger.info(f'[{callback.from_user.id}, {callback.from_user.username}: ' + \
                f'{callback.data}]')

    await callback.answer('')
    await callback.message.answer('Введи имя')
    await state.update_data(prev_state=await state.get_state())
    await state.set_state(AdminDrinkOrder.set_nickname)


# @router.message(Command('add_order'),
#                 F.from_user.id.in_(admins_list),
#                 StateFilter(None, DrinkOrder.order_done))
# async def cmd_add_order(message: Message, state: FSMContext):
#     logger.info(f'[{message.from_user.id}, {message.from_user.username}: ' + \
#                 f'{message.text}]')

#     await message.answer('Введи имя')
#     await state.update_data(prev_state=await state.get_state())
#     await state.set_state(AdminDrinkOrder.set_name)


@router.message(StateFilter(AdminDrinkOrder.set_nickname))
async def add_drink(message: Message, state: FSMContext):
    logger.info(f'[{message.from_user.id}, {message.from_user.username}: ' + \
                f'{message.text}]')

    await message.answer(text='Введи название напитка')
    await state.update_data(nickname=message.text)
    await state.set_state(AdminDrinkOrder.set_drink)


@router.message(StateFilter(AdminDrinkOrder.set_drink))
async def admin_create_order(message: Message, state: FSMContext):
    logger.info(f'[{message.from_user.id}, {message.from_user.username}: ' + \
                f'{message.text}]')

    await message.answer('Записал ✅',
                         reply_markup=admins_kb)
    data = await state.get_data()
    nickname = data.get('nickname')
    drink = message.text
    gsheets.send_order_to_google_sheet(nickname, drink)
    await state.set_state(data['prev_state'])
