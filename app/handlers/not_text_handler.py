from aiogram import F, Router
from aiogram.types import Message
import logging

from handlers import messages
from handlers.drink_order import DrinkOrder


router = Router(name=__name__)
logger = logging.getLogger(__name__)


# Считывание id чата SKU_RUN при добавлении в него
# @router.message(F.content_type == ContentType.NEW_CHAT_MEMBERS)
# async def new_chat_members(message: Message):
#     logger.info(f'[{message.from_user.id}, {message.from_user.username}: ' + \
#                 f'{message.content_type}]')

#     logger.info(f'GROUP_ID={message.chat.id}')
#     with open('.env', 'a') as fp:
#         fp.write(f'GROUP_ID={message.chat.id}\n')


@router.message(~F.text)
async def other_messages_handler(message: Message):
    logger.info(f'[{message.from_user.id}, {message.from_user.username}: ' + \
                f'{message.content_type}]')

    content_type = messages.content_types_dict[str(message.content_type)]
    await message.answer(text=messages.incorrect_type.format(content_type))
