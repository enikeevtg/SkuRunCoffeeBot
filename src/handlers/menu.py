# Обработка заказа напитка

from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from utils import gsheets
from keyboards import menu_kb_builder
from db_handler import db_models
from handlers import messages, start, vars, check_list


router = Router()


# FSM states
class OrderDrink(StatesGroup):
    choosing_drink = State()
    choosing_option = State()


async def check_list_handler(message: Message):
    if message.from_user.id in check_list:
        name = db_models.get_cup_name_from_person_table(message.from_user.id) 
        await message.answer(f'Ты регистрировался под именем {name}. ' +\
                             'Давай сперва поменяем его. Жми /edit')
        check_list.remove(message.from_user.id)
        with open('handlers/__init__.py', 'w') as fp:
            fp.write(f'check_list = {check_list}')
        return True
    return False


@router.message(StateFilter(None), Command('menu'))
async def cmd_menu(message: Message, state: FSMContext):
    # Предложение некоторым пользователям поменять имя
    if await check_list_handler(message) is True:
        return

    # Временная проверка наличия пользователя в базе данных
    user = db_models.get_cup_name_from_person_table(message.from_user.id)
    if user == None:
        await start.cmd_start(message, state)
        return

    order = vars.orders.get(message.from_user.id, None)
    if order:
        await message.answer(str(order['name']) +
                             ', твой заказ (' +
                             str(order['drink'].lower()) +
                             ') уже отправил баристе. ' +
                             'Он будет с нетерпением ждать, ' +
                             'когда ты вернёшься с пробежки 🤗')
    else:
        await message.answer(text=messages.choose_drink, 
                             reply_markup=await menu_kb_builder(vars.drink_names))
        await state.set_state(OrderDrink.choosing_drink)


@router.message(OrderDrink.choosing_drink, F.text.in_(vars.drink_names))
async def drink_chosen(message: Message, state: FSMContext):
    if message.text == 'Фильтр-кофе':
        await message.answer(messages.success_order_msg +
                             str(message.text.lower()),
                             reply_markup=ReplyKeyboardRemove())
        create_order(message)
        await state.clear()
        return

    options = vars.americano_options if message.text == 'Американо' \
                                     else vars.rosehip_options
    await message.answer(text=messages.choose_option,
                         reply_markup=await menu_kb_builder(options))
    await state.set_state(OrderDrink.choosing_option)


@router.message(OrderDrink.choosing_drink)
async def drink_choosen_incorrectly(message: Message):
    await message.answer(text=messages.try_again,
                         reply_markup=await menu_kb_builder(vars.drink_names))


@router.message(OrderDrink.choosing_option, F.text.in_(vars.drink_names +
                                                       vars.americano_options + 
                                                       vars.rosehip_options))
async def option_chosen(message: Message, state: FSMContext):
    await message.answer(messages.success_order_msg + str(message.text.lower()),
                         reply_markup=ReplyKeyboardRemove())
    create_order(message)
    await state.clear()


@router.message(OrderDrink.choosing_option)
async def option_choosen_incorrectly(message: Message, state: FSMContext):
    await message.answer(text=messages.try_again,
                         reply_markup=await menu_kb_builder(vars.drink_names))
    await state.set_state(OrderDrink.choosing_drink)


def create_order(message):
    cup_name = db_models.get_cup_name_from_person_table(message.from_user.id)
    vars.orders[message.chat.id] = {'name': cup_name, 'drink': message.text}

    order_id = vars.order_id
    vars.order_id += 1
    gsheets.send_order_to_google_sheet(order_id, cup_name, message.text)
