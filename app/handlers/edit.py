# Редактирование имени бегуна

from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from db_handler import db_models
from handlers import start, messages, vars


router = Router()


# FSM states
class Edition(StatesGroup):
    set_new_name = State()


@router.message(Command('edit'))
async def cmd_edit(message: Message, state: FSMContext):
    # Временная проверка наличия пользователя в базе данных
    user = db_models.get_cup_name_from_person_table(message.from_user.id)
    if user == None:
        await start.cmd_start(message, state)
        return

    await message.answer(f'{user}, ниже введи новое имя ✍️')
    await state.update_data(prev_state=await state.get_state())
    await state.set_state(Edition.set_new_name)


@router.message(Edition.set_new_name)
async def set_new_name(message: Message, state: FSMContext):
    if message.content_type != "text":
        await message.answer(messages.incorrect_message_type)
    elif message.text.replace(' ', '').isalpha() is False:
        await message.answer(messages.incorrect_name)
    else:
        user_id = message.from_user.id
        cup_name = message.text.strip()
        reply_msg = 'Ну всё, в следующий раз на твоём стаканчике ' + \
                    'мы напишем ' + str(cup_name) + ' 😁'
        if message.from_user.id not in vars.orders:
            reply_msg = 'Ну всё, поменял твоё имя на ' + \
                        str(cup_name) + ' 😁\n' + \
                        'Теперь жми /menu и выбирай свой напиток'

        await message.answer(reply_msg)
        db_models.update_cup_name_in_person_table(user_id, cup_name)
        await state.update_data(name=cup_name)
        await state.set_state((await state.get_data())['prev_state'])
