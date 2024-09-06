# Центральный файл бота. Обработка бесполезных сообщений

import asyncio
from bot import bot, dp
import messages
import time

# from bot_gsheets import *
# from cmd_start import *
# from cmd_menu import *
# from cmd_name import *
# from cmd_edit import *
from handlers.start import *


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


# async def the_order_has_already_been_placed(message):
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
# async def other_msg(message):
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


if __name__ == '__main__':
    asyncio.run(main())    
