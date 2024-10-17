from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from database import requests as rq
from handlers import start


router = Router()


@router.message(Command('name'))
async def cmd_name(message: Message, state: FSMContext):
    # Временная проверка наличия пользователя в базе данных
    cur_cup_name = await rq.get_user_cup_name(message.from_user.id)
    if cur_cup_name == None:
        await start.cmd_start(message, state)
        return

    await message.answer('На твоём стаканчике будет имя ' +
                         cur_cup_name + ' ❤️')
