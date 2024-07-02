import telebot
import botconfig

bot = telebot.TeleBot(botconfig.token)


@bot.message_handler(commands=['start'])
def start(message):
    start_message = 'Рост\n' + 'время на 5000\n' + \
                     'степень кофемании и любимый сорт напитка.\n(c)FranticDog'
    bot.send_message(message.chat.id, start_message)

bot.polling(non_stop=True)
