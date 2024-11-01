import asyncio

from admin import add_order, admins_main
from bot import bot, dp
from handlers import bio, drink_order, not_text_handler, start 
from database.models import db_main
from utils import gsheets


async def main():
    gsheets.init_google_sheet()
    await db_main()
    dp.include_routers(not_text_handler.router, start.router,
                       admins_main.router, add_order.router,
                       drink_order.router, bio.router)
    await admins_main.admins_bot_start_notification(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
