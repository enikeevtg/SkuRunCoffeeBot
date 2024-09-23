# Админ

from aiogram import Bot
from decouple import config
from db_handler import db_models
from handlers import messages
from keyboards import table_kb_builder


admins_list = [int(admin_id) for admin_id in config('ADMINS').split(',')]


async def send_gsheet_link(bot: Bot):
    for admin_id in admins_list:
        user_name = db_models.get_cup_name_from_person_table(admin_id)
        await bot.send_message(admin_id,
                               user_name + ', я родился 🤗\n' +
                               messages.commands_admin,
                               reply_markup=await table_kb_builder())
