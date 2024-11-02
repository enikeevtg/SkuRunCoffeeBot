from aiogram.filters import BaseFilter
from aiogram.types import Message
from decouple import config


class IsAdmin(BaseFilter):
    def __init__(self):
        self.admins_ids = [int(id) for id in config('ADMINS').split(',')]

    async def __call__(self, message: Message):
        return message.from_user.id in self.admins_ids
