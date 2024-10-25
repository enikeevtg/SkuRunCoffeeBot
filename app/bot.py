import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from decouple import config
import logging

from admin import add_order, admins_main
from handlers import bio, drink_order, not_text_handler, start 
from database.models import db_main
from utils import gsheets


async def main():
    gsheets.clear_google_sheet()
    await db_main()
    bot = Bot(token=config('TOKEN'))
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_routers(not_text_handler.router, start.router,
                       admins_main.router, add_order.router,
                       drink_order.router, bio.router)
    await admins_main.admins_bot_start_notification(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logfile = open('skurun.log', 'w')
    format = "%(asctime)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s"
    logging.basicConfig(stream=logfile, level=logging.INFO, format=format)
    logger = logging.getLogger(__name__)
    asyncio.run(main())
