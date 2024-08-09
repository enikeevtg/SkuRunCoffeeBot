# Набор общих функций


from bot import bot
import config


def get_cup_name_from_user(message, next_step_function):
    if message.content_type != "text":
        bot.send_message(message.chat.id, config.name_not_text_msg)
        bot.register_next_step_handler(message,
                                       get_cup_name_from_user,
                                       next_step_function)
    elif message.text.replace(' ', '').isalpha() is False:
        bot.send_message(message.chat.id, config.name_false_msg)
        bot.register_next_step_handler(message,
                                       get_cup_name_from_user,
                                       next_step_function)
    else:
        next_step_function(message)
