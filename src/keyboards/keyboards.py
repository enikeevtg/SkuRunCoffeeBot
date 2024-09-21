# Клавиатуры

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
import handlers.vars as vars

def menu_kb_builder(names_list: int) -> ReplyKeyboardMarkup:
    buttons_list = []
    for name in names_list:
        buttons_list.append([KeyboardButton(text=name)])
    keyboard = ReplyKeyboardMarkup(
                  keyboard=buttons_list,
                  resize_keyboard=True,
                  # one_time_keyboard=True,
                  input_field_placeholder='Выбирай из списка напитков'
                  )

    return keyboard
