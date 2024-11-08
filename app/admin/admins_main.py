from aiogram import Bot
from aiogram import F, Router
from aiogram.types import Message
import logging

from filters.is_admin import is_admin
from database import requests as rq
from keyboards import i_am_admin_btn_text, admins_kb


logger = logging.getLogger(__name__)


async def admins_bot_start_notification(bot: Bot):
    for admin_id in is_admin.admins_ids:
        nickname = await rq.get_nickname(admin_id)
        await bot.send_message(admin_id, nickname + ', я родился 🤗\n',
                               reply_markup=admins_kb)


router = Router()


@router.message(F.text == i_am_admin_btn_text, is_admin)
async def display_admins_keyboard(message: Message):
    await message.answer(text='Твои секретные возможности 🤫',
                         reply_markup=admins_kb)


@router.message(F.text == i_am_admin_btn_text)
async def display_admins_keyboard(message: Message):
    logger.info(f'[{message.from_user.id}, {message.from_user.username}: ' + \
                f'{message.text}]')

    await message.answer(text='Доступ запрещён 🤨')
