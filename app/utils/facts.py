from aiogram.types import CallbackQuery
from aiogram.utils.chat_action import ChatActionSender
import asyncio
# import random


from bot import bot


title = '☕️ <b>Кофейный факт:</b>\n'
fact_1 = 'Способ приготовления кофе «Американо» появился во время Второй мировой войны. Американские военные не могли пить крепкий европейский кофе и просили разбавить его водой.'
fact_2 = 'В XVII и XVIII веках кофе запрещали в разных европейских странах. Например, в Швеции запретили не только напиток, но и посуду для него.'
# facts = [fact_1, fact_2]
# fact = random.choice(facts)


async def send_fact(callback: CallbackQuery):
    async with ChatActionSender(bot=bot, chat_id=callback.from_user.id,
                                action='typing'):
        await asyncio.sleep(1)
        await callback.message.answer(title + fact_2)
