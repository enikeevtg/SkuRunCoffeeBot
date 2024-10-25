# Клавиатуры

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
import logging

from database.requests import get_categoties, get_category_items


logger = logging.getLogger(__name__)


# inline keyboard buttons callback data
back_to_categories_btn_cb = 'back_to_categories'


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
    keyboard.add(InlineKeyboardButton(text='⬅️ Назад в основное меню',
                                      callback_data=back_to_categories_btn_cb))
    return keyboard.adjust(1).as_markup()
