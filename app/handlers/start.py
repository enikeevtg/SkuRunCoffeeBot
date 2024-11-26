from aiogram import F, Router
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ContentType, Message
import logging

from bot import admins_ids
from database import requests as rq
from handlers import messages
from keyboards import main_kb, admins_main_kb


router = Router()
logger = logging.getLogger(__name__)


# FSM states
class Registration(StatesGroup):
    set_nickname = State()


@router.message(CommandStart(), StateFilter(None))
async def cmd_start(message: Message, state: FSMContext):
    logger.info(f'[{message.from_user.id}, {message.from_user.username}: ' + \
                 f'{message.text}]')

    nickname = await rq.get_nickname(message.from_user.id)
    if not nickname:
        await message.answer(messages.register_request)
        await state.set_state(Registration.set_nickname)
        return

    await lets_go(message)


@router.message(F.content_type == ContentType.TEXT,
                Registration.set_nickname)
async def set_nickname(message: Message, state: FSMContext):
    logger.info(f'[{message.from_user.id}, {message.from_user.username}: ' + \
                 f'{message.text}]')

    if message.text.replace(' ', '').isalpha() is False:
        await message.answer(messages.incorrect_nickname)
    else:
        await lets_go(message)
        await rq.set_user(message.from_user, message.text.strip())
        await state.clear()


async def lets_go(message: Message):
    await message.answer(f'Поехали! 🚀',
                         reply_markup=admins_main_kb
                                      if message.from_user.id
                                      in admins_ids
                                      else main_kb)


async def redirection_test(message: Message):
    import aiohttp
    from decouple import config

    from bot import bot
    from keyboards import redirection_kb

    goods = [
        '26/11/2024 Поставщик_1 Точка_1 с 12:00 до 15:00',
        '27/11/2024 Поставщик_2 Точка_2 с 09:00 до 11:00',
        '28/11/2024 Поставщик_3 Точка_3 с 11:00 до 12:00',
        '29/11/2024 Поставщик_4 Точка_4 с 15:00 до 17:00',
        '30/11/2024 Поставщик_5 Точка_2 с 10:00 до 11:00',
    ]
    for good in goods:
        await bot.send_message(chat_id=config('GROUP_ID'),
                               text=good,
                               reply_markup=redirection_kb)

    url = f"https://api.telegram.org/bot{config('TOKEN')}/sendMessage"
    params = {
        "chat_id": 819128057,
        "text": f'{message.chat.id}'
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, params=params) as response:
        # async with session.request('POST', url, params=params) as response:
            print(f'start.py: 73 {response.status=}. {message.chat.id=}')
