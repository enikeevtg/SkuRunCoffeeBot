from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot import admins_ids
from handlers.drink_order import DrinkOrder
from keyboards import admins_main_kb


router = Router(name=__name__)


@router.message(
    Command("cancel"),
    F.from_user.id.in_(admins_ids),
    ~StateFilter(DrinkOrder.order_in_process),
)
async def cmd_cancel(message: Message, state: FSMContext):
    data = await state.get_data()
    await state.set_state(data.get("prev_state", None))
    await message.answer(text="Действие отменено", reply_markup=admins_main_kb)
