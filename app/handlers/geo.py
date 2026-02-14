from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, ContentType, Message
from aiogram.utils.chat_action import ChatActionSender
import asyncio
from datetime import datetime
import logging

from bot import bot
from keyboards import start_location_tracking, stop_location_tracking
from keyboards import tracking_start_kb, tracking_stop_kb
from handlers import messages

router = Router()
logger = logging.getLogger(__name__)
trackings = dict()


too_small_live_period = "Слишком маленький период отслеживания геопозиции. Поделись геолокацией хотя бы на 1 час"
location_tracking_started = "Уахаха, ты на крючке. Теперь от меня не спрячешься 😈\nЕсли ты будешь филонить и отсиживаться в кустах, пока все бегают, я узнаю и наябедничаю Юре 😝"
countdown = "\n\nReady, Set..."
location_tracking_in_process = "🏃🏻‍♂️🏃🏻‍♀️🏃🏼‍♂️🏃🏻🏃🏽‍♀️🏃🏽‍♂️🏃🏼🏃🏼‍♀️"


# FSM states
class Workout(StatesGroup):
    running = State()


@router.message(F.content_type == ContentType.LOCATION)
async def geolocation_handler(message: Message):
    logger.info(
        f"[{message.from_user.id}, {message.from_user.username}: "
        f"{message.content_type}]"
    )

    if (
        message.location.live_period is None
        or message.location.live_period < 3599
    ):
        await message.answer(messages.too_small_live_period)
    else:
        await message.answer(
            messages.location_tracking_started + messages.countdown,
            reply_markup=tracking_start_kb,
        )


@router.callback_query(F.data == start_location_tracking)
async def start_training(callback: CallbackQuery, state: FSMContext):
    logger.info(
        f"[{callback.from_user.id}, {callback.from_user.username}: "
        f"{callback.data}]"
    )

    await callback.answer()
    await callback.message.edit_text(messages.location_tracking_started)
    await callback.message.answer(
        messages.location_tracking_in_process, reply_markup=tracking_stop_kb
    )
    trackings[callback.from_user.id] = []
    await state.update_data(prev_state=await state.get_state())
    await state.set_state(Workout.running)


@router.edited_message(F.content_type == ContentType.LOCATION, Workout.running)
async def edited_message_handler(message: Message):
    time = datetime.now().time()
    lat = message.location.latitude
    lon = message.location.longitude
    trackings[message.from_user.id].append((time, lat, lon))

    logger.info(
        f"[{message.from_user.id}, {message.from_user.username}: "
        f"{time} {lat} {lon}]"
    )


@router.callback_query(F.data == stop_location_tracking)
async def stop_training(callback: CallbackQuery, state: FSMContext):
    logger.info(
        f"[{callback.from_user.id}, {callback.from_user.username}: "
        f"{callback.data}]"
    )

    data = await state.get_data()
    await state.set_state(data["prev_state"])
    await callback.answer()
    async with ChatActionSender(
        bot=bot, chat_id=callback.from_user.id, action="typing"
    ):
        status_line = []
        await callback.message.edit_text(
            "Обработка трека\n" "".join(status_line)
        )
        for _ in range(15):
            await asyncio.sleep(0.3)
            status_line.append("█")
            await callback.message.edit_text(
                "Обработка трека\n" "".join(status_line)
            )

        with open(f"track_{callback.from_user.id}.txt", "w") as fp:
            for el in trackings[callback.from_user.id]:
                fp.write(f"{el[0]}: {el[1]} {el[2]}\n")
        await asyncio.sleep(3)
        await callback.message.edit_text("Трек обработан")
