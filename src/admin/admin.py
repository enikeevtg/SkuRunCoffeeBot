# Админ

import asyncio
from aiogram import Bot, Router

from decouple import config
from db_handler import db


router = Router()


async def send_gsheet_link(bot: Bot):
    admins = [int(admin_id) for admin_id in config('ADMINS').split(',')]
    for admin in admins:
        user_name = db.get_cup_name_from_person_table(admin)
        await bot.send_message(admin,
                               user_name + ', я родился 🤗\n' +
                               'Вот тут ссылка на гугл-таблицу 👇\n' +
                               'https://docs.google.com/spreadsheets/d/' + config('SPREADSHEET_ID') + '/edit')
