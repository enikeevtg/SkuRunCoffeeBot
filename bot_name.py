from bot import bot
import db


@bot.message_handler(commands=['name'])
def show_current_cup_name(message):
    cup_name = db.get_cup_name_from_person_table(message.from_user.id)
    bot.send_message(message.chat.id,
                     'На твоём следующем стаканчике мы напишем ' +
                                       str(cup_name) + ' ❤️')
