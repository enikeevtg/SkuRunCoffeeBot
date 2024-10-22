from aiogram import Bot
from decouple import config


admins_list = [int(admin_id) for admin_id in config('ADMINS').split(',')]


from database import requests as rq
from keyboards import admin_kb_builder


async def send_gsheet_link(bot: Bot):
    for admin_id in admins_list:
        user_name = await rq.get_user_cup_name(admin_id)
        await bot.send_message(admin_id,
                               user_name + ', я родился 🤗\n',
                               reply_markup=await admin_kb_builder())
