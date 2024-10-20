import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from decouple import config
# import logging

import admin
from admin import add_order, table
from db_handler import db_models
from handlers import start, menu, edit, name, cancel
from utils import gsheets


from aiogram.client.session.aiohttp import AiohttpSession
session = AiohttpSession(proxy="http://proxy.server:3128")


async def main():
    gsheets.clear_google_sheet()
    db_models.create_person_table()

    bot = Bot(token=config('TOKEN'), session=session)
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_routers(cancel.router)
    dp.include_routers(start.router, menu.router, add_order.router,
                       edit.router, name.router, table.router)

    await admin.send_gsheet_link(bot)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    # logfile = open('skurun.log', 'w')
    # format = "%(asctime)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s"
    # logging.basicConfig(stream=logfile, level=logging.DEBUG, format=format)
    # logger = logging.getLogger(__name__)
    asyncio.run(main())
