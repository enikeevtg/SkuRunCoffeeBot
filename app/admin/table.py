# Команда открытия таблицы заказов

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from admin import admins_list
from keyboards import table_kb_builder


router = Router()


@router.message(Command('table'),
                F.from_user.id.in_(admins_list))
async def cmd_table(message: Message):
    await message.answer('Таблица заказов',
                         reply_markup=await table_kb_builder())
