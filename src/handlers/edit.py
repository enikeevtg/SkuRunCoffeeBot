# Редактирование имени бегуна

from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from db_handler import db
from handlers import start, messages, vars


router = Router()


# FSM states
class Edition(StatesGroup):
    set_new_name = State()


@router.message(StateFilter(None), Command('edit'))
async def cmd_edit(message: Message, state: FSMContext):
    user = db.get_cup_name_from_person_table(message.from_user.id)
    if user == None:
        await start.cmd_start(message, state)
        return

    await message.answer(str(user) + messages.edit_name)
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
        db.update_cup_name_in_person_table(user_id, cup_name)
        await state.clear()
