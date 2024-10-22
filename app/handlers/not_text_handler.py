from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.types import ContentType, Message
import logging

from handlers import messages
from handlers.menu import DrinkOrder


router = Router()
logger = logging.getLogger(__name__)


@router.message(F.content_type != ContentType.TEXT,
                StateFilter(None, DrinkOrder.order_done))
async def other_messages_handler_excluded_states(message: Message):
    logger.info(f'[{message.from_user.id}, {message.from_user.username}: ' + \
                f'{message.content_type}]')


@router.message(F.content_type != ContentType.TEXT)
async def other_messages_handler(message: Message):
    logger.info(f'[{message.from_user.id}, {message.from_user.username}: ' + \
                f'{message.content_type}]')

    content_type = messages.content_types_dict[str(message.content_type)]
    await message.answer(text=messages.incorrect_type.format(content_type))
