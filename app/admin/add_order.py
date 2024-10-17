# Добавление заказа вручную

from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from admin import admins_list
from utils import gsheets
from keyboards import table_kb_builder


router = Router()


# FSM states
class AdminOrderDrink(StatesGroup):
    set_name = State()
    set_drink = State()
    order_done = State()


@router.message(Command('add_order'),
                F.from_user.id.in_(admins_list))
async def cmd_add_order(message: Message, state: FSMContext):
    await message.answer('Введи имя')
    await state.update_data(prev_state=await state.get_state())
    await state.set_state(AdminOrderDrink.set_name)


@router.message(StateFilter(AdminOrderDrink.set_name))
async def add_drink(message: Message, state: FSMContext):
    await message.answer(text='Введи название напитка')
    await state.update_data(cup_name=message.text)
    await state.set_state(AdminOrderDrink.set_drink)


@router.message(StateFilter(AdminOrderDrink.set_drink))
async def admin_create_order(message: Message, state: FSMContext):
    await message.answer('Записал. Можешь проверить в таблице',
                         reply_markup=await table_kb_builder())
    data = await state.get_data()
    cup_name = data.get('cup_name')
    drink = message.text
    gsheets.send_order_to_google_sheet(cup_name, drink)
    await state.set_state(data['prev_state'])
