import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from decouple import config
import logging

import admin
from admin import add_order
from database.models import db_main
from handlers import start, name, menu, edit, not_text_handler 
from utils import gsheets


from aiogram.client.session.aiohttp import AiohttpSession
session = AiohttpSession(proxy="http://proxy.server:3128")


async def main():
    gsheets.clear_google_sheet()
    await db_main()
    bot = Bot(token=config('TOKEN'), session=session)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_routers(not_text_handler.router, start.router, 
                       menu.router, add_order.router, edit.router, name.router)
    await admin.send_gsheet_link(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logfile = open('skurun.log', 'w')
    format = "%(asctime)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s"
    logging.basicConfig(stream=logfile, level=logging.INFO, format=format)
    logger = logging.getLogger(__name__)
    asyncio.run(main())
