import logging


logfile = open('log.txt', 'w')
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', stream=logfile)
logger = logging.getLogger(__name__)


import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from decouple import config
from handlers import start, menu, edit, name


async def main():
    bot = Bot(token=config('TOKEN'))
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_routers(start.router, menu.router, edit.router, name.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())


order_id = int(config('FIRST_ORDER_ROW'))
# временная база заказов в текущий день
# {user_id: {
#            'name': 'Тагир',
#            'drink': 'Шиповник'
#           }
# }
orders = {}


# КАТЕГОРИИ И ПОДКАТЕГОРИИ НАПИТКОВ
drink_names = ['Американо', 'Шиповник', 'Фильтр-кофе']
amerincano_options = ['Американо', 'Американо со сливками',
                      'Американо с овсяным молоком']
rosehip_options = ['Шиповник', 'Шиповник с мёдом', 'Шиповник со льдом',
                   'Шиповник с мёдом и льдом']

# amerincano_options = ['Сливки', 'Овсяное молоко 🥛',
#                       'Просто американо, пожалуйста ☕️']
# rosehip_options = ['Лёд 🧊', 'Мёд 🍯', 'Всего и побольше 😋 🧊 🍯',
#                    'Просто шип, пожалуйста']


# def the_order_has_already_been_placed(message):
#     ordered_drink = config.orders.get(message.from_user.id, None)
#     if ordered_drink != None:
#         bot.send_message(message.chat.id,
#                          str(ordered_drink['name']) +
#                          ', твой заказ (' +
#                          str(ordered_drink['drink'].lower()) +
#                          ') уже отправил баристе. ' +
#                          'Отдыхай и наслаждайся беганутой атмосферой 🤗')
#     else:
#         bot.send_message(message.chat.id, config.commans_msg)


# @bot.message_handler()
# def other_msg(message):
#     all_drinks_list = [drink.lower() for drink in (config.types_of_coffee +
#                                                    config.amerincano_options +
#                                                    config.rosehip_options)]
#     if message.text.strip().lower() in all_drinks_list:
#         the_order_has_already_been_placed(message)
#     else:
#         bot.send_message(message.chat.id, 'Моя твоя не понимать, нащальнике\n'
#                                           + config.commans_msg)
    
#     # print([time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(message.date)),
#     #        message.from_user.username,
#     #        message.text])
