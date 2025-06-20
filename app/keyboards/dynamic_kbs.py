import asyncio
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
import logging
from typing import Dict, List

from database import requests as rq


logger = logging.getLogger(__name__)


back_to_categories_btn_cb = "back_to_categories"


async def items_kbs_dict() -> Dict[str, List[InlineKeyboardMarkup]]:
    items_kbs: Dict[str, List[InlineKeyboardMarkup]] = dict()
    categories = await rq.get_categories()
    for category in categories:
        items = await rq.get_category_items(category.id)
        items_kbs[f"category_{category.id}_{category.name}"] = items_kb(items)
    return items_kbs


def items_kb(items: List[rq.DrinkItem]) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    for item in items:
        keyboard.button(
            text=item.name, callback_data=f"item_{item.id}_{item.name}"
        )
    keyboard.button(
        text="⬅️ Назад в основное меню", callback_data=back_to_categories_btn_cb
    )
    return keyboard.adjust(1).as_markup()


def categories_kb_builder(
    items_kbs: Dict[str, List[InlineKeyboardMarkup]],
) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    for category in items_kbs.keys():
        keyboard.button(text=category.split("_")[2], callback_data=category)
    return keyboard.adjust(1).as_markup()


items_kbs: Dict[str, List[InlineKeyboardMarkup]] = asyncio.run(
    items_kbs_dict()
)
categories_kb = categories_kb_builder(items_kbs)
