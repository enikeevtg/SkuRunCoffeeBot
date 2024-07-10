import telebot
from telebot import types
import config
import db
from bot_token import token


bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start(message):
    db.create_person_table()

    user = db.get_cup_name_from_person_table(message.from_user.id)
    if user:
        bot.send_message(message.chat.id,
                         f'О, а я тебя знаю! Ты - {user} 😄')
        show_drink_types_keyboard(message, 'Давай тогда выберем напиток')
    else:
        # bot.send_message(message.chat.id, config.starting_msg)
        bot.send_message(message.chat.id, config.cup_name_query_msg)
        bot.register_next_step_handler(message, get_cup_name_from_user)


def get_cup_name_from_user(message):
    if (message.text.rstrip().isalpha() is False):
        bot.register_next_step_handler(message, get_cup_name_from_user)
        bot.send_message(message.chat.id, config.name_false_msg)
    else:
        registration(message)


def registration(message):
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    cup_name = message.text.strip()
    user = db.Person(user_id, username, first_name, last_name, cup_name)
    db.insert_user_to_person_table(user)
    show_drink_types_keyboard(message, config.name_true_msg)


@bot.message_handler(commands=['edit'])
def edit(message):
    bot.send_message(message.chat.id, config.edit_name_msg)
    


@bot.message_handler(commands=['menu'])
def menu(message):
    show_drink_types_keyboard(message, config.choose_drink)


def show_drink_types_keyboard(message, reply_message):
    ordered_drink = config.orders.get(message.from_user.id, None)
    if ordered_drink is None:
        drinks_keyboard_generator(message, reply_message)
    else:
        bot.send_message(message.chat.id,
                         str(ordered_drink['name']) +
                         ', твой заказ (' +
                         str(ordered_drink['drink'].lower()) +
                         ') уже отправил баристе. ' +
                         'Отдыхай и наслаждайся беганутой атмосферой 🤗')


def drinks_keyboard_generator(message, reply_message):
    markup = types.ReplyKeyboardMarkup()
    for coffee in config.types_of_coffee:
        markup.add(types.KeyboardButton(coffee))
    bot.register_next_step_handler(message, show_options_keyboard)
    bot.send_message(message.chat.id, reply_message,
                      reply_markup=markup)
    

def show_options_keyboard(message):
    if message.text not in config.types_of_coffee:
        drinks_keyboard_generator(message, config.try_again)
        return

    if message.text == 'Фильтр-кофе':
        create_order(message, None)
        return

    options = config.amerincano_options
    if message.text == 'Шиповник':
        options = config.rosehip_options

    options_keyboard_generator(message, options, config.choose_option)


def options_keyboard_generator(message, options, reply_message):
    markup = types.ReplyKeyboardMarkup()
    for option in options:
        markup.add(types.KeyboardButton(option))
    bot.register_next_step_handler(message, create_order, options)
    bot.send_message(message.chat.id, reply_message, reply_markup=markup)
    

def create_order(message, options):
    if message.text not in (config.amerincano_options +
                            config.rosehip_options +
                            config.types_of_coffee):
        options_keyboard_generator(message, options, config.try_again)
        return

    cup_name = db.get_cup_name_from_person_table(message.from_user.id)
    config.orders[message.chat.id] = {'name': cup_name,
                                      'drink': message.text}

    user_data = db.select_user_from_person_table(message.from_user.id)[0]
    with open("orders.txt", "a") as fp:
        fp.write(str(db.Person(*user_data[1:6])) +
                 '   Напиток: ' +
                 message.text +
                 '\n\n')


    bot.send_message(message.chat.id,
                     config.order_msg + str(message.text.lower()))


def order_again(message):
    ordered_drink = config.orders.get(message.from_user.id, None)
    if ordered_drink != None:
        bot.send_message(message.chat.id,
                         str(ordered_drink['name']) +
                         ', твой заказ (' +
                         str(ordered_drink['drink'].lower()) +
                         ') уже отправил баристе. ' +
                         'Отдыхай и наслаждайся атмосферой 🤗')
    else:
        bot.send_message(message.chat.id, 'Жми /menu')


@bot.message_handler()
def other_msg(message):
    if message.text.strip() in (config.types_of_coffee +
                                config.amerincano_options +
                                config.rosehip_options):
        order_again(message)
    else:
        bot.send_message(message.chat.id, 'Моя твоя не понимать, нащальнике')


bot.polling(non_stop=True)
