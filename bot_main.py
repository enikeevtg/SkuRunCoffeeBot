from telebot import types
from bot import bot
import config
import db
from bot_token import token
import time


from bot_start import *
from bot_menu import *
from bot_name import *
from bot_edit import *


def the_order_has_already_been_placed(message):
    ordered_drink = config.orders.get(message.from_user.id, None)
    if ordered_drink != None:
        bot.send_message(message.chat.id,
                         str(ordered_drink['name']) +
                         ', твой заказ (' +
                         str(ordered_drink['drink'].lower()) +
                         ') уже отправил баристе. ' +
                         'Отдыхай и наслаждайся беганутой атмосферой 🤗')
    else:
        bot.send_message(message.chat.id, config.commans_msg)


@bot.message_handler()
def other_msg(message):
    all_drinks_list = [drink.lower() for drink in (config.types_of_coffee +
                                                   config.amerincano_options +
                                                   config.rosehip_options)]
    if message.text.strip().lower() in all_drinks_list:
        the_order_has_already_been_placed(message)
    else:
        bot.send_message(message.chat.id, 'Моя твоя не понимать, нащальнике\n'
                                          + config.commans_msg)
    
    # print([time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(message.date)),
    #        message.from_user.username,
    #        message.text])


bot.polling(non_stop=True)
