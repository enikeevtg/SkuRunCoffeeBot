# Обработка запроса на отоборажение имени бегуна


from bot import bot
import bot_start
import db


@bot.message_handler(commands=['name'])
def show_current_cup_name(message):
    user = db.get_cup_name_from_person_table(message.from_user.id)
    if user == None:
        bot_start.start(message)
        return

    cup_name = db.get_cup_name_from_person_table(message.from_user.id)
    bot.send_message(message.chat.id,
                     'На твоём стаканчике будет имя ' + 
                     str(cup_name) + ' ❤️')
