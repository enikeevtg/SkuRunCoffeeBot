from aiogram import F, Router
from aiogram.types import Message
import logging

from bot import admins_ids
from database import requests as rq
from keyboards import i_am_admin_btn_text, admins_kb


router = Router(name=__name__)
logger = logging.getLogger(__name__)


@router.message(F.text == i_am_admin_btn_text, F.from_user.id.in_(admins_ids))
async def display_admins_keyboard(message: Message):
    await message.answer(text='Твои секретные возможности 🤫',
                         reply_markup=admins_kb)


@router.message(F.text == i_am_admin_btn_text)
async def display_admins_keyboard(message: Message):
    logger.info(f'[{message.from_user.id}, {message.from_user.username}: ' + \
                f'{message.text}]')

    await message.answer(text='Доступ запрещён 🤨')
