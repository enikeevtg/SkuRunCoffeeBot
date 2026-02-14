from aiogram import F, Router
from aiogram.types import CallbackQuery
import logging
import random

from bot import bot, daily_runners
from keyboards import dice_cb


router = Router(name=__name__)
logger = logging.getLogger(__name__)


@router.callback_query(F.data == dice_cb)
async def dice(callback: CallbackQuery):
    logger.info(
        f"[{callback.from_user.id}, {callback.from_user.username}: "
        f"{callback.data}]"
    )

    await callback.answer()
    winner = random.choice(daily_runners)
    await callback.message.answer(
        text=f"Выйграл {winner["nickname"]} (@{winner["username"]})",
    )

    await bot.send_message(
        chat_id=winner["tg_id"],
        text="Поздравляю! Только что ты выйграл <s>ааааааавтомобиль</s> наш скромный подарок 🥳\nГромко прокричи на всю кофейню, что ты победитель, чтобы все знали, кто тут батя 😄"
    )
    logger.info(f"Победитель: {winner}")
