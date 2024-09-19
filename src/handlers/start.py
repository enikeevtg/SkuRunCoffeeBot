# Регистрация бегуна при первом входе в бота


from aiogram import Router
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from db_handler import db
from handlers import messages


router = Router()


class Registration(StatesGroup):
    set_name = State()


@router.message(StateFilter(None), CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    db.create_person_table()

    user = db.get_cup_name_from_person_table(message.from_user.id)
    if user:
        await message.answer(f'О, а я тебя знаю! Ты - {user} 😄\n\n' +
                             messages.commands)
    else:
        await message.answer(messages.register_request)
        await state.set_state(Registration.set_name)


@router.message(Registration.set_name)
async def set_name(message: Message, state: FSMContext):
    if message.content_type != "text":
        await message.answer(messages.incorrect_message_type)
    elif message.text.replace(' ', '').isalpha() is False:
        await message.answer(messages.incorrect_name)
    else:
        user_data = get_user_data_from_message(message)
        user = db.Person(*user_data)
        await message.answer(f'{user_data[4]}, я тебя запомнил 😄\n\n' +
                             messages.commands)
        db.insert_user_to_person_table(user)
        await state.clear()


def get_user_data_from_message(message: Message):
    user_id = message.from_user.id             # 0
    username = message.from_user.username      # 1
    first_name = message.from_user.first_name  # 2
    last_name = message.from_user.last_name    # 3
    cup_name = message.text.strip()            # 4
    return (user_id, username, first_name, last_name, cup_name)
