# Добавление заказа вручную

from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from admin import admins_list
from utils import gsheets
from keyboards import menu_kb_builder
from db_handler import db
from handlers import menu, messages, vars


router = Router()


# FSM states
class AdminOrderDrink(StatesGroup):
    set_name = State()
    choosing_drink = State()
    choosing_option = State()
    order_done = State()


@router.message(StateFilter(None), Command('add_order'))
async def cmd_add_order(message: Message, state: FSMContext):
    if message.from_user.id not in admins_list:
        message.answer('Недостаточно прав для использования данной команды')
        return

    await message.answer('Введи имя')
    await state.set_state(AdminOrderDrink.set_name)


@router.message(StateFilter(AdminOrderDrink.set_name))
async def choose_drink(message: Message, state: FSMContext):
    await message.answer('Выбери напиток из списка',
                         reply_markup=await menu_kb_builder(vars.drink_names))
    await state.update_data(name=message.text)
    await state.set_state(AdminOrderDrink.choosing_drink)
    await message.answer(state)


@router.message(StateFilter(AdminOrderDrink.choosing_drink),
                F.text.in_(vars.drink_names))
async def admin_drink_chosen(message: Message, state: FSMContext):
    if message.text == 'Фильтр-кофе':
        await message.answer('Записал. Можешь проверить в таблице',
                             reply_markup=ReplyKeyboardRemove())
        await state.update_data(drink=message.text)
        await state.set_state(AdminOrderDrink.order_done)
        await create_order(message, state)
        return

    options = vars.americano_options if message.text == 'Американо' \
                                     else vars.rosehip_options
    await message.answer(text=messages.choose_option,
                         reply_markup=await menu_kb_builder(options))
    await state.update_data(drink=message.text)
    await state.set_state(AdminOrderDrink.choosing_option)


@router.message(StateFilter(AdminOrderDrink.choosing_drink))
async def admin_drink_choosen_incorrectly(message: Message):
    await message.answer(text=messages.try_again,
                         reply_markup=await menu_kb_builder(vars.drink_names)
                         )


@router.message(AdminOrderDrink.choosing_option,
                F.text.in_(vars.drink_names +
                           vars.americano_options +
                           vars.rosehip_options))
async def admin_option_chosen(message: Message, state: FSMContext):
    await message.answer('Записал. Можешь проверить в таблице',
                         reply_markup=ReplyKeyboardRemove())
    await state.update_data(drink=message.text)
    await state.set_state(AdminOrderDrink.order_done)
    await create_order(message, state)


@router.message(AdminOrderDrink.choosing_option)
async def admin_option_choosen_incorrectly(message: Message, state: FSMContext):
    await message.answer(text=messages.try_again,
                         reply_markup=await menu_kb_builder(vars.drink_names)
                         )
    await state.set_state(AdminOrderDrink.choosing_drink)


@router.message(AdminOrderDrink.order_done)
async def create_order(message: Message, state: FSMContext):
    data = await state.get_data()
    cup_name = data.get('name')
    drink = data.get('drink')
    order_id = vars.order_id
    vars.order_id += 1
    gsheets.send_order_to_google_sheet(order_id, cup_name, drink)
    await state.clear()
