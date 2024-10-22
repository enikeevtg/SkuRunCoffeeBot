# Клавиатуры

from aiogram.types import (KeyboardButton, ReplyKeyboardMarkup,
                           InlineKeyboardButton, InlineKeyboardMarkup)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from decouple import config
import logging

from database.requests import get_categoties, get_category_items
from admin import admins_list


logger = logging.getLogger(__name__)


def main_kb_builder(tg_id: int) -> ReplyKeyboardMarkup:
    menu_btn = KeyboardButton(text='Выбрать напиток')
    profile_btn = KeyboardButton(text='Профиль')
    btns_list = [[menu_btn], [profile_btn]]

    # добавка для админской клавиатуры
    if tg_id in admins_list:
        logger.info(f'[{admins_list=}, {tg_id=}')
        btns_list.append([KeyboardButton(text='Я админ')])
    
    return ReplyKeyboardMarkup(keyboard=btns_list,
                               resize_keyboard=True)


async def admin_kb_builder() -> InlineKeyboardMarkup:
    add_order_btn = InlineKeyboardButton(
                            text='Добавить напиток бегуна без телеги',
                            callback_data='add_order')
    table_url = 'https://docs.google.com/spreadsheets/d/' + \
                config('SPREADSHEET_ID') + '/edit'
    open_table_btn = InlineKeyboardButton(text='Открыть таблицу заказов',
                                          url=table_url)
    return InlineKeyboardMarkup(inline_keyboard=[[add_order_btn],
                                                 [open_table_btn]])


async def categories_kb_builder() -> InlineKeyboardMarkup:
    categories = await get_categoties()
    keyboard = InlineKeyboardBuilder()
    for category in categories:
        keyboard.add(
            InlineKeyboardButton(text=category.name,
                                 callback_data=f'category_{category.id}'))
    return keyboard.adjust(1).as_markup()


async def items_kb_builder(category_id: int) -> InlineKeyboardMarkup:
    items = await get_category_items(category_id)
    keyboard = InlineKeyboardBuilder()
    for item in items:
        keyboard.add(InlineKeyboardButton(text=item.name,
                                          callback_data=f'item_{item.id}'))
    keyboard.add(InlineKeyboardButton(text='В основное меню',
                                      callback_data='to_menu'))
    return keyboard.adjust(1).as_markup()


async def confirmation_kb_builder():
    no_btn = InlineKeyboardButton(text='❌', callback_data='reject')
    yes_btn = InlineKeyboardButton(text='✅', callback_data='confirm')
    return InlineKeyboardMarkup(inline_keyboard=[[no_btn, yes_btn]])
