import logging


logfile = open('log.txt', 'w')
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', stream=logfile)
logger = logging.getLogger(__name__)


import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from decouple import config
from handlers import start, menu


async def main():
    bot = Bot(token=config('TOKEN'))
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_routers(start.router, menu.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())


# временная база заказов в текущий день
# {chat_id: {
#            'name': 'Тагир',
#            'order': 'Шиповник'
#           }
# }
orders = {}

