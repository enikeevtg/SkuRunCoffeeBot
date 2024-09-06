# Редактирование имени бегуна


from bot import bot
import cmd_start
import db
import messages
import utils.utils as utils


@bot.message_handler(commands=['edit'])
def edit(message):
    user = db.get_cup_name_from_person_table(message.from_user.id)
    if user == None:
        cmd_start.start(message)
        return

    cup_name = db.get_cup_name_from_person_table(message.from_user.id)
    bot.send_message(message.chat.id, str(cup_name) + messages.edit_name_msg)
    bot.register_next_step_handler(message,
                                   utils.get_cup_name_from_user,
                                   edit_cup_name)


def edit_cup_name(message):
    user_id = message.from_user.id
    cup_name = message.text.strip()
    db.update_cup_name_in_person_table(user_id, cup_name)

    # user_data = db.select_user_from_person_table(user_id)
    # print(str(db.Person(*user_data[1:6])))

    reply_msg = 'Ну всё, в следующий раз на твоём стаканчике ' + \
                'мы напишем ' + str(cup_name) + ' 😁'
    if user_id not in messages.orders:
        reply_msg = 'Ну всё, поменял твоё имя на ' + \
                    str(cup_name) + ' 😁\n' + \
                    'Теперь жми /menu и выбирай свой напиток'

    bot.send_message(message.chat.id, reply_msg)
