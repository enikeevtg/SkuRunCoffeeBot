from aiogram.filters import BaseFilter
from aiogram.types import Message
from bot import group_id


class IsSkuRunGroup(BaseFilter):
    def __init__(self) -> None:
        self.group_id = group_id

    async def __call__(self, message: Message) -> bool:
        return message.chat.id == self.group_id


is_skurun_group = IsSkuRunGroup()
