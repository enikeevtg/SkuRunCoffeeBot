from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
import logging

from handlers.start import Registration
from handlers.menu import DrinkOrder


router = Router()
logger = logging.getLogger(__name__)


cmd_cancel_exclusions = [
    Registration.set_name,
    DrinkOrder.order_confirmation,
    DrinkOrder.order_done
]
    

@router.message(Command('cancel'))
async def cmd_cancel(message: Message, state: FSMContext):
    logger.info(f'[{message.from_user.id}, {message.from_user.username}: ' + \
                 f'{message.text}]')

    if await state.get_state() in cmd_cancel_exclusions: 
        await message.answer('Отмена действия невозможна')
        return

    await message.answer('Действие отменено',
                         reply_markup=ReplyKeyboardRemove())
    await state.clear()
