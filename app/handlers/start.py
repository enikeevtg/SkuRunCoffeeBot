# Регистрация бегуна при первом входе в бота

from aiogram import F, Router
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ContentType, Message

from database import requests as rq
from handlers import messages


router = Router()


# FSM states
class Registration(StatesGroup):
    set_name = State()


@router.message(StateFilter(None), CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    user = await rq.get_user_cup_name(message.from_user.id)
    if user:
        await message.answer(f'{user}, мы с тобой уже знакомы 😄\n\n' +
                             messages.commands)
    else:
        await message.answer(messages.register_request)
        await state.set_state(Registration.set_name)


@router.message(Registration.set_name, F.content_type == ContentType.TEXT)
async def set_name(message: Message, state: FSMContext):
    if message.text.replace(' ', '').isalpha() is False:
        await message.answer(messages.incorrect_name)
    else:
        await rq.set_user(message.from_user, message.text.strip())
        await message.answer(f'{message.text.strip()}, я тебя запомнил 😄\n\n' +
                             messages.commands)
        await state.clear()
