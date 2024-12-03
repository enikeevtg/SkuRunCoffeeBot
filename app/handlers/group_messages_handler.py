from aiogram import F, Router
from aiogram.types import Message
import logging

from bot import group_id
logger = logging.getLogger(__name__)

router = Router(name=__name__)


@router.message(F.chat.id == group_id)
async def ignore_group_chat_all_messages(message: Message):
    logger.info(f'[{message.from_user.id}, {message.from_user.username}: ' + \
                f'{message.text}]')
