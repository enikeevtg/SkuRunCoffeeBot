from aiogram import F, Router
from aiogram.types import ContentType, Message

from handlers import messages
from handlers.messages import content_types_dict, incorrect_type


router = Router()


@router.message(F.content_type != ContentType.TEXT)
async def other_messages_handler(message: Message):
    content_type = content_types_dict[str(message.content_type)]
    await message.answer(text=messages.incorrect_type.format(content_type))
