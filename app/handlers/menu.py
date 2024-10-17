from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from utils import gsheets

from database import requests as rq
from handlers import messages, start, vars
from keyboards import menu_kb_builder, confirmation_kb_builder


router = Router()


# FSM states
class DrinkOrder(StatesGroup):
    choosing_drink = State()
    choosing_option = State()
    order_confirmation = State()
    order_done = State()


@router.message(Command('menu'),
                StateFilter(DrinkOrder.order_done))
async def cmd_menu(message: Message, state: FSMContext):
    data = await state.get_data()
    name: str = data['name']
    drink: str = data['drink']
    await message.answer(messages.order_done.format(name, drink.lower()))


@router.message(Command('menu'), StateFilter(None))
async def cmd_menu(message: Message, state: FSMContext):

    # Временная проверка наличия пользователя в базе данных
    cup_name = await rq.get_user_cup_name(message.from_user.id)
    if cup_name == None:
        await start.cmd_start(message, state)
        return

    await message.answer(text=messages.choose_drink, 
                         reply_markup=await menu_kb_builder(vars.drink_names))
    await state.update_data(name=cup_name)
    await state.set_state(DrinkOrder.choosing_drink)


@router.message(DrinkOrder.choosing_drink, F.text.in_(vars.drink_names))
async def drink_chosen(message: Message, state: FSMContext):
    drink = message.text
    await state.update_data(drink=drink)

    if drink == 'Фильтр-кофе':
        await option_chosen(message, state)
        return

    options = vars.drink_options[drink]
    await message.answer(text=messages.choose_option,
                         reply_markup=await menu_kb_builder(options))
    await state.set_state(DrinkOrder.choosing_option)


@router.message(DrinkOrder.choosing_drink)
async def drink_chosen_incorrectly(message: Message, state: FSMContext):
    await message.answer(text=messages.try_again,
                         reply_markup=await menu_kb_builder(vars.drink_names))
    await state.set_state(DrinkOrder.choosing_drink)


@router.message(DrinkOrder.choosing_option,
                F.text.in_(vars.americano_options + vars.rosehip_options))
async def option_chosen(message: Message, state: FSMContext):
    await state.update_data(drink=message.text)
    await order_confirmation(message, state)


@router.message(DrinkOrder.choosing_option)
async def option_chosen_incorrectly(message: Message, state: FSMContext):
    drink = (await state.get_data())['drink']
    options = vars.drink_options[drink]
    await message.answer(text=messages.try_again,
                         reply_markup=await menu_kb_builder(options))
    await state.set_state(DrinkOrder.choosing_option)


async def order_confirmation(message: Message, state: FSMContext):
    data = await state.get_data()
    await state.set_state(DrinkOrder.order_confirmation)
    await message.answer(f'Твой заказ:\n{data["name"]} — {data["drink"]}',
                         reply_markup=ReplyKeyboardRemove())
    await message.answer('Отправляю баристе?',
                         reply_markup=await confirmation_kb_builder())


@router.callback_query(DrinkOrder.order_confirmation, F.data == 'create_order')
async def create_order(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await callback.message.edit_text(text=messages.success_order_msg +
                                     str(data['drink']).lower())
    await callback.answer('')
    await state.set_state(DrinkOrder.order_done)
    vars.orders[callback.from_user.id] = data
    gsheets.send_order_to_google_sheet(data['name'], data['drink'])


@router.callback_query(DrinkOrder.order_confirmation, F.data == 'cancel_order')
async def cancel_order(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text='Окей, давай начнём сначала! ' +
                                     messages.commands)
                                #, reply_markup=await confirmation_kb_builder())
    await callback.answer('')
    await state.clear()
