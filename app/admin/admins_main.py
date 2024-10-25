from aiogram import Bot
from aiogram import F, Router
from aiogram.types import Message

from admin import admins_list
from database import requests as rq
from keyboards import i_am_admin_btn_text, admins_kb


async def admins_bot_start_notification(bot: Bot):
    for admin_id in admins_list:
        user_name = await rq.get_nickname(admin_id)
        await bot.send_message(admin_id, user_name + ', я родился 🤗\n',
                               reply_markup=admins_kb)


router = Router()


@router.message(F.text == i_am_admin_btn_text,
                F.from_user.id.in_(admins_list))
async def display_admins_keyboard(message: Message):
    await message.answer(text='Твои секретные возможности 🤫',
                         reply_markup=admins_kb)


@router.message(F.text == i_am_admin_btn_text)
async def display_admins_keyboard(message: Message):
    await message.answer(text='Не понял, что ты тут забыл 🤨')
