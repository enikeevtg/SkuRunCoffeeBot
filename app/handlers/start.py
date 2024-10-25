from aiogram import F, Router
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ContentType, Message
import logging

from admin import admins_list
from database import requests as rq
from handlers import messages
from keyboards import main_kb, admins_main_kb


router = Router()
logger = logging.getLogger(__name__)


# FSM states
class Registration(StatesGroup):
    set_nickname = State()


@router.message(CommandStart(),
                StateFilter(None))
async def cmd_start(message: Message, state: FSMContext):
    logger.info(f'[{message.from_user.id}, {message.from_user.username}: ' + \
                 f'{message.text}]')

    user_cup_name = await rq.get_nickname(message.from_user.id)
    if not user_cup_name:
        await message.answer(messages.register_request)
        await state.set_state(Registration.set_nickname)

    await message.answer(f'Поехали! 🚀',
                         reply_markup=admins_main_kb
                                      if message.from_user.id in admins_list
                                      else main_kb)


@router.message(F.content_type == ContentType.TEXT,
                Registration.set_nickname)
async def set_nickname(message: Message, state: FSMContext):
    logger.info(f'[{message.from_user.id}, {message.from_user.username}: ' + \
                 f'{message.text}]')

    if message.text.replace(' ', '').isalpha() is False:
        await message.answer(messages.incorrect_nickname)
    else:
        await rq.set_user(message.from_user, message.text.strip())
        await state.clear()
