import asyncio
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
import logging

from utils.drinks_menu import create_drinks_menu


logger = logging.getLogger(__name__)


back_to_categories_btn_cb = 'back_to_categories'
drinks = asyncio.run(create_drinks_menu())

def categories_kb_builder() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    for category in drinks.keys():
        keyboard.button(text=category.split('_')[2],
                        callback_data=category)
    return keyboard.adjust(1).as_markup()


categories_kb = categories_kb_builder()


def items_kb_builder(category_key: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    for item in drinks[category_key]:
        keyboard.button(text=item.split('_')[2],
                        callback_data=item)
    keyboard.button(text='⬅️ Назад в основное меню',
                    callback_data=back_to_categories_btn_cb)
    return keyboard.adjust(1).as_markup()
