import asyncio

from admin import add_order, admins_main
from bot import bot, dp
from database.models import db_main
from handlers import (bio, drink_order, not_text_handler, start, 
                      group_messages_handler)
from utils.notifications import (send_admins_bot_start_notification,
                                 send_group_bot_start_notification)


async def main():
    await db_main()
    dp.include_routers(group_messages_handler.router,
                       not_text_handler.router, start.router,
                       admins_main.router, add_order.router,
                       drink_order.router, bio.router)
    await send_admins_bot_start_notification()
    await send_group_bot_start_notification()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
