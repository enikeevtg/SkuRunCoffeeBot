from bot import bot
import db
import config
import bot_common_functions as common


@bot.message_handler(commands=['edit'])
def edit(message):
    cup_name = db.get_cup_name_from_person_table(message.from_user.id)
    bot.send_message(message.chat.id, str(cup_name) + config.edit_name_msg)
    bot.register_next_step_handler(message,
                                   common.get_cup_name_from_user,
                                   edit_cup_name)


def edit_cup_name(message):
    user_id = message.from_user.id
    cup_name = message.text.strip()
    db.update_cup_name_in_person_table(user_id, cup_name)

    user_data = db.select_user_from_person_table(user_id)
    print(str(db.Person(*user_data[1:6])))

    reply_msg = 'Ну всё, на твоём следующем стаканчике ' + \
                'мы напишем ' + str(cup_name) + ' 😁'
    if user_id not in config.orders:
        reply_msg = 'Ну всё, на твоём следующем стаканчике ' + \
                    'мы напишем ' + str(cup_name) + ' 😁\n' +  \
                    'Теперь выбирай свой напиток из /menu'

    bot.send_message(message.chat.id, reply_msg)
