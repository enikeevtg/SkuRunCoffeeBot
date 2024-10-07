# Команда выхода пользователя из процесса взаимодействия

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from handlers.start import Registration
from handlers.menu import DrinkOrder


router = Router()


cmd_cancel_exclusions = [
    Registration.set_name,
    DrinkOrder.order_confirmation,
    DrinkOrder.order_done
]
    

@router.message(Command('cancel'))
async def cmd_cancel(message: Message, state: FSMContext):
    if await state.get_state() in cmd_cancel_exclusions: 
        await message.answer('Отмена невозможна')
        return

    await message.answer('Отмена', reply_markup=ReplyKeyboardRemove())
    await state.clear()
