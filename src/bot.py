import logging


logfile = open('log.txt', 'w')
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', stream=logfile)
logger = logging.getLogger(__name__)


import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from decouple import config
from db_handler import db
from handlers import start, menu, edit, name


# Для запуска на pythonanywhere.com:
# from aiogram.client.session.aiohttp import AiohttpSession
# session = AiohttpSession(proxy="http://proxy.server:3128")


async def send_gsheet_to_admins(bot: Bot):
    admins = [int(admin_id) for admin_id in config('ADMINS').split(',')]
    for admin in admins:
        user_name = db.get_cup_name_from_person_table(admin)
        await bot.send_message(admin,
                               user_name + ', я родился 🤗\n' +
                               'Вот тут ссылка на гугл-таблицу 👇\n' +
                               'https://docs.google.com/spreadsheets/d/' + config('SPREADSHEET_ID') + '/edit')


async def main():
    bot = Bot(token=config('TOKEN'))
    # Для запуска на pythonanywhere.com:
    # bot = Bot(token=config('TOKEN'), session=session)
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_routers(start.router, menu.router, edit.router, name.router)

    await send_gsheet_to_admins(bot)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())




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
