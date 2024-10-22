from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ContentType, Message
import logging

from database import requests as rq
from handlers import start, messages
from handlers.menu import DrinkOrder

router = Router()
logger = logging.getLogger(__name__)


# FSM states
class Edition(StatesGroup):
    set_new_name = State()


@router.message(Command('edit'),
                StateFilter(None, DrinkOrder.order_done))
async def cmd_edit(message: Message, state: FSMContext):
    logger.info(f'[{message.from_user.id}, {message.from_user.username}: ' + \
                 f'{message.text}]')

    # Временная проверка наличия пользователя в базе данных
    user = await rq.get_user_cup_name(message.from_user.id)
    if user == None:
        await start.cmd_start(message, state)
        return

    await message.answer(f'{user}, ниже введи новое имя ✍️')
    await state.update_data(prev_state=await state.get_state())
    await state.set_state(Edition.set_new_name)


@router.message(F.content_type == ContentType.TEXT,
                Edition.set_new_name)
async def set_new_name(message: Message, state: FSMContext):
    logger.info(f'[{message.from_user.id}, {message.from_user.username}: ' + \
                 f'{message.text}]')

    if message.text.replace(' ', '').isalpha() is False:
        await message.answer(messages.incorrect_name)
    else:
        cup_name = message.text.strip()
        reply_msg = 'Ну всё, в следующий раз на твоём стаканчике ' + \
                    'мы напишем ' + str(cup_name) + ' 😁'
        if (await state.get_data())['prev_state'] is None:
            reply_msg = 'Ну всё, поменял твоё имя на ' + \
                        str(cup_name) + ' 😁\n' + \
                        'Теперь жми /menu и выбирай свой напиток'

        await message.answer(reply_msg)
        await rq.update_user_cup_name(message.from_user.id, cup_name)
        await state.update_data(name=cup_name)
        await state.set_state((await state.get_data())['prev_state'])
