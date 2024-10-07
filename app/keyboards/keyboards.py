# Клавиатуры

from aiogram.types import (KeyboardButton, ReplyKeyboardMarkup,
                           InlineKeyboardButton, InlineKeyboardMarkup)
from decouple import config


async def menu_kb_builder(names_list: int) -> ReplyKeyboardMarkup:
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


async def table_kb_builder() -> InlineKeyboardMarkup:
    table_url = 'https://docs.google.com/spreadsheets/d/' +\
                config('SPREADSHEET_ID') + '/edit'
    open_table_btn = InlineKeyboardButton(text='Открыть таблицу', url=table_url)
    return InlineKeyboardMarkup(inline_keyboard=[[open_table_btn]])


async def confirmation_kb_builder():
    no_btn = InlineKeyboardButton(text='❌', callback_data='cancel_order')
    yes_btn = InlineKeyboardButton(text='✅', callback_data='create_order')
    return InlineKeyboardMarkup(inline_keyboard=[[no_btn, yes_btn]])
