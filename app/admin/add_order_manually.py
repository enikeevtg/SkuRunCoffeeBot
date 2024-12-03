# Добавление заказа вручную админом

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message
import logging

from bot import spreadsheet
from keyboards import add_order_manually_btn_cb, admins_kb


router = Router(name=__name__)
logger = logging.getLogger(__name__)


class AdminDrinkOrder(StatesGroup):
    set_nickname = State()
    set_drink = State()
    order_done = State()


@router.callback_query(F.data == add_order_manually_btn_cb)
async def add_order_manually(callback: CallbackQuery, state: FSMContext):
    logger.info(f'[{callback.from_user.id}, {callback.from_user.username}: ' + \
                f'{callback.data}]')

    await callback.answer()
    await callback.message.answer('Введи имя')
    await state.update_data(prev_state=await state.get_state())
    await state.set_state(AdminDrinkOrder.set_nickname)


@router.message(StateFilter(AdminDrinkOrder.set_nickname))
async def add_drink(message: Message, state: FSMContext):
    logger.info(f'[{message.from_user.id}, {message.from_user.username}: ' + \
                f'{message.text}]')

    await message.answer(text='Введи название напитка')
    await state.update_data(user_nickname=message.text)
    await state.set_state(AdminDrinkOrder.set_drink)


@router.message(StateFilter(AdminDrinkOrder.set_drink))
async def admin_create_order(message: Message, state: FSMContext):
    logger.info(f'[{message.from_user.id}, {message.from_user.username}: ' + \
                f'{message.text}]')

    await message.answer('Записал ✅',
                         reply_markup=admins_kb)
    data = await state.get_data()
    user_nickname = data.get('user_nickname')
    drink = message.text
    spreadsheet.send_order(message.from_user.id,
                           message.from_user.username,
                           user_nickname,
                           drink)
    await state.set_state(data['prev_state'])
