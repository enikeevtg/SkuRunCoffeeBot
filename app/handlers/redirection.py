from aiogram import F, Router
from aiogram.types import CallbackQuery
import logging

from keyboards import redirection_btn


router = Router()
logger = logging.getLogger(__name__)


@router.callback_query(F.data == redirection_btn.callback_data)
async def redirect(callback: CallbackQuery):
    logger.info(f'[{callback.from_user.id}, {callback.from_user.username}: ' + \
                f'{callback.data}]')

    bot_me = await callback.bot.me()
    await callback.answer(url=f't.me/{bot_me.username}?start=0')
