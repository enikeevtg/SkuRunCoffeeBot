# Обработка запроса на отоборажение имени бегуна


from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from db_handler import db
from handlers import start


import sys
sys.path.append('../')
import bot
import messages
# import db


router = Router()


@router.message(Command('name'))
async def cmd_name(message: Message, state: FSMContext):
    user = db.get_cup_name_from_person_table(message.from_user.id)
    if user == None:
        await start.cmd_start(message, state)
        return

    cup_name = db.get_cup_name_from_person_table(message.from_user.id)
    await message.answer('На твоём стаканчике будет имя ' +
                         str(cup_name) + ' ❤️')
