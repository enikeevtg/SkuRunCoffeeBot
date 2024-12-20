import asyncio

import admin
import handlers
from bot import bot, dp
from database.models import db_main
from utils.notifications import (send_admins_bot_start_notification,
                                 send_group_bot_start_notification)


async def main():
    await db_main()
    dp.include_routers(admin.router, handlers.router)
    await send_admins_bot_start_notification()
    await send_group_bot_start_notification()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
