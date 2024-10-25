from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ContentType, CallbackQuery, Message
import logging

from database import requests as rq
from handlers import start
from handlers import messages
from keyboards import profile_btn_text, bio_kb, edit_name_cb


router = Router()
logger = logging.getLogger(__name__)


class NameEdition(StatesGroup):
    set_new_name = State()


@router.message(F.text == profile_btn_text)
async def display_user_bio(message: Message, state: FSMContext):
    logger.info(f'[{message.from_user.id}, {message.from_user.username}: ' + \
                 f'{message.text}]')
    
    # Временная проверка наличия пользователя в базе данных
    cur_cup_name = await rq.get_nickname(message.from_user.id)
    if cur_cup_name == None:
        await start.cmd_start(message, state)
        return

    await message.answer(messages.user_bio.format(message.from_user.id,
                                                  cur_cup_name),
                         reply_markup=bio_kb)


@router.callback_query(F.data == edit_name_cb)
async def edit_name(callback: CallbackQuery, state: FSMContext):
    logger.info(f'[{callback.from_user.id}, {callback.from_user.username}: ' + \
                f'{callback.data}]')

    await callback.answer('')
    await callback.message.answer(text=messages.input_new_nickname)
    await state.update_data(prev_state=await state.get_state())
    await state.set_state(NameEdition.set_new_name)


@router.message(F.content_type == ContentType.TEXT,
                NameEdition.set_new_name)
async def set_new_name(message: Message, state: FSMContext):
    logger.info(f'[{message.from_user.id}, {message.from_user.username}: ' + \
                 f'{message.text}]')

    if message.text.replace(' ', '').isalpha() is False:
        await message.answer(messages.incorrect_nickname)
    else:
        nickname = message.text.strip()
        await message.answer(text=messages.set_nickname_done
                                          .format(nickname))
        await rq.update_nickname(message.from_user.id, nickname)
        await state.set_state((await state.get_data())['prev_state'])
