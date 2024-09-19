# Клавиатуры

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def menu_kb(names_list: int) -> ReplyKeyboardMarkup:
    buttons_list = []
    for name in names_list:
        buttons_list.append([KeyboardButton(text=name)])
    keyboard = ReplyKeyboardMarkup(keyboard=buttons_list,
                                   resize_keyboard=True,
                                   one_time_keyboard=True)
    return keyboard
