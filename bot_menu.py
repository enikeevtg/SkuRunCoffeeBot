# Обработка заказа напитка


from bot import bot
import config
import db
import bot_gsheets as gsheets
from telebot import types


@bot.message_handler(commands=['menu'])
def menu(message):
    ordered_drink = config.orders.get(message.from_user.id, None)
    if ordered_drink is None:
        drinks_keyboard_generator(message, config.choose_drink_msg)
    else:
        bot.send_message(message.chat.id,
                         str(ordered_drink['name']) +
                         ', твой заказ (' +
                         str(ordered_drink['order'].lower()) +
                         ') уже отправил баристе. ' +
                         'Отдыхай и наслаждайся беганутой атмосферой 🤗')


def drinks_keyboard_generator(message, reply_message):
    types_markup = types.ReplyKeyboardMarkup()
    for coffee in config.types_of_coffee:
        types_markup.add(types.KeyboardButton(coffee))
    bot.send_message(message.chat.id, reply_message,
                     reply_markup=types_markup)
    bot.register_next_step_handler(message, show_options_keyboard)
    

def show_options_keyboard(message):
    if message.text not in config.types_of_coffee:
        drinks_keyboard_generator(message, config.try_again_msg)
        return

    if message.text == 'Фильтр-кофе':
        create_order(message, None)
        return

    options = config.amerincano_options
    if message.text == 'Шиповник':
        options = config.rosehip_options

    options_keyboard_generator(message, options, config.choose_option_msg)


def options_keyboard_generator(message, options, reply_message):
    options_markup = types.ReplyKeyboardMarkup()
    for option in options:
        options_markup.add(types.KeyboardButton(option))
    bot.send_message(message.chat.id, reply_message,
                     reply_markup=options_markup)
    bot.register_next_step_handler(message, create_order, options)
    

def create_order(message, options):
    if message.text not in (config.amerincano_options +
                            config.rosehip_options +
                            config.types_of_coffee):
        options_keyboard_generator(message, options, config.try_again_msg)
        return

    # Удаление клавиатуры у пользователя
    empty_markup = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id,
                     config.order_msg + str(message.text.lower()),
                     reply_markup=empty_markup)

    cup_name = db.get_cup_name_from_person_table(message.from_user.id)
    config.orders[message.chat.id] = {'name': cup_name,
                                      'order': message.text}
    
    order_id = config.order_id
    config.order_id += 1
    gsheets.send_order_to_google_sheet(order_id, cup_name, message.text)

    # Отправка данных заказа в текстовый файл для первого тестирования
    user_data = db.select_user_from_person_table(message.from_user.id)
    if user_data:
        with open("orders.txt", "a") as fp:
            fp.write(str(db.Person(*user_data[1:6])) +
                    '   Напиток: ' +
                    message.text +
                    '\n\n')

