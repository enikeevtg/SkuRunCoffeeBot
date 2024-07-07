import telebot
from telebot import types
import config
import db
from token import token


bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start(message):
    db.create_person_table()

    user = get_cup_name_from_db(message.from_user.id)
    if user:
        bot.send_message(message.chat.id,
                         f"О, а я тебя знаю! Ты - {user} 😄")
        coffee_choosing(message, 'Давай тогда выберем напиток')
    else:
        bot.send_message(message.chat.id, config.starting_msg)
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
    coffee_choosing(message, config.name_true_msg)


@bot.message_handler(commands=['coffee'])
def coffee_menu(message):
    coffee_choosing(message, 'Выбери напиток из списка 👇')


def coffee_choosing(message, reply_message):
    ordered_drink = config.order.get(message.from_user.id, None)
    if ordered_drink != None:
        bot.send_message(message.chat.id,
                         str(ordered_drink['name']) +
                         ', твой заказ (' +
                         str(ordered_drink['drink'].lower()) +
                         ') уже отправил баристе. ' +
                         'Отдыхай и наслаждайся беганутой атмосферой 🤗')
    else:
        markup = types.ReplyKeyboardMarkup()
        for coffee in config.types_of_coffee:
            markup.add(types.KeyboardButton(coffee))
        bot.register_next_step_handler(message, option_choosing)
        bot.send_message(message.chat.id, reply_message,
                        reply_markup=markup)


def option_choosing(message):
    if message.text not in config.types_of_coffee:
        bot.send_message(message.chat.id, 'У нас такого нет. Жми /coffee')
        return

    if message.text == 'Фильтр-кофе':
        create_order(message)
        return

    options = config.amerincano_options
    if message.text == 'Шиповник':
        options = config.rosehip_options

    markup = types.ReplyKeyboardMarkup()
    for option in options:
        markup.add(types.KeyboardButton(option))
    bot.register_next_step_handler(message, create_order)
    bot.send_message(message.chat.id,
                     f'''Что-нибудь добавим в {message.text.lower()}?''',
                     reply_markup=markup)


def create_order(message):
    if message.text not in (config.amerincano_options +
                            config.rosehip_options +
                            config.types_of_coffee):
        bot.send_message(message.chat.id, 'У нас такого нет. Жми /coffee')
        return

    cup_name = get_cup_name_from_db(message.from_user.id)
    config.order[message.chat.id] = {'name': cup_name,
                                     'drink': message.text}
    print(config.order)
    bot.send_message(message.chat.id,
                     config.order_msg + str(message.text.lower()))


def get_cup_name_from_db(user_id):
    user = db.select_user_from_table(user_id)
    return user[0][5] if len(user) > 0 else None 


bot.polling(non_stop=True)


@bot.callback_query_handler(func=lambda call: call.data == 'print_users')
def callback(call):
    with open("callback.log", 'w') as fp:
        fp.write(str(call))
    # bot.send_message(call.message.chat.id, 'Привет')
    connection, cursor = db.db_connection()
    cursor.execute('SELECT * FROM person')
    person_table = cursor.fetchall()

    persons = 'Пользователи:\n'
    for el in person_table:
        persons += f'id: {el[0]}, uid: {el[1]}, uname: {el[2]}, fname: {el[3]}, lname: {el[4]}, cname: {el[5]}\n'
    
    db.db_closing(connection, cursor)

    bot.send_message(call.message.chat.id, persons)
