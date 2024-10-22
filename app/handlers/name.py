from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
import logging

from database import requests as rq
from handlers import start
from handlers.menu import DrinkOrder


router = Router()
logger = logging.getLogger(__name__)


@router.message(Command('name'),
                StateFilter(None, DrinkOrder.order_done))
async def cmd_name(message: Message, state: FSMContext):
    logger.info(f'[{message.from_user.id}, {message.from_user.username}: ' + \
                 f'{message.text}]')
    
    # Временная проверка наличия пользователя в базе данных
    cur_cup_name = await rq.get_user_cup_name(message.from_user.id)
    if cur_cup_name == None:
        await start.cmd_start(message, state)
        return

    await message.answer('На твоём стаканчике будет имя ' +
                         cur_cup_name + ' ❤️')
