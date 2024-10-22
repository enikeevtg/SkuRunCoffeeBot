# Команда открытия таблицы заказов (исключено из функционала)

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
import logging

from admin import admins_list
from keyboards import table_kb_builder


router = Router()
logger = logging.getLogger(__name__)


@router.message(Command('table'),
                F.from_user.id.in_(admins_list))
async def cmd_table(message: Message):
    logger.info(f'[{message.from_user.id}, {message.from_user.username}: ' + \
                f'{message.text}]')

    await message.answer('Таблица заказов',
                         reply_markup=await table_kb_builder())
