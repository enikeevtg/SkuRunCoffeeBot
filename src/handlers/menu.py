# Обработка заказа напитка


from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from utils import gsheets
from keyboards.keyboards import menu_kb
from handlers import start


import sys
sys.path.append('../')
import bot
import messages
import db


router = Router()


class OrderDrink(StatesGroup):
    choosing_drink = State()
    choosing_option = State()


@router.message(StateFilter(None), Command('menu'))
async def cmd_menu(message: Message, state: FSMContext):
    user = db.get_cup_name_from_person_table(message.from_user.id)
    if user == None:
        await start.cmd_start(message, state)
        return

    order: str = bot.orders.get(message.from_user.id, None)
    if order:
        await message.answer(str(order['name']) +
                             ', твой заказ (' +
                             str(order['drink'].lower()) +
                             ') уже отправил баристе. ' +
                             'Он будет с нетерпением ждать, ' +
                             'когда ты вернёшься с пробежки 🤗')
    else:
        await message.answer(text=messages.choose_drink, 
                             reply_markup=menu_kb(bot.drink_names))
        await state.set_state(OrderDrink.choosing_drink)


@router.message(OrderDrink.choosing_drink, F.text.in_(bot.drink_names))
async def drink_chosen(message: Message, state: FSMContext):
    if message.text == 'Фильтр-кофе':
        await message.answer(messages.order_msg + str(message.text.lower()))
        create_order(message)
        await state.clear()
        return

    options = bot.amerincano_options if message.text == 'Американо' \
                                     else bot.rosehip_options
    await message.answer(text=messages.choose_option,
                         reply_markup=menu_kb(options))
    await state.set_state(OrderDrink.choosing_option)


@router.message(OrderDrink.choosing_drink)
async def drink_choosen_incorrectly(message: Message):
    await message.answer(text=messages.try_again,
                         reply_markup=menu_kb(bot.drink_names)
                         )
    

@router.message(OrderDrink.choosing_option, F.text.in_(bot.drink_names +
                                                       bot.amerincano_options + 
                                                       bot.rosehip_options))
async def option_chosen(message: Message, state: FSMContext):
    await message.answer(messages.order_msg + str(message.text.lower()))
    create_order(message)
    await state.clear()


@router.message(OrderDrink.choosing_option)
async def option_choosen_incorrectly(message: Message, state: FSMContext):
    await message.answer(text=messages.try_again,
                      reply_markup=menu_kb(bot.drink_names)
                      )
    await state.set_state(OrderDrink.choosing_drink)


def create_order(message):
    cup_name = db.get_cup_name_from_person_table(message.from_user.id)
    bot.orders[message.chat.id] = {'name': cup_name, 'drink': message.text}

    order_id = bot.order_id
    bot.order_id += 1
    gsheets.send_order_to_google_sheet(order_id, cup_name, message.text)