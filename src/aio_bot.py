import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from __token import token
from aiogram.filters import CommandStart, Command

dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: types.Message):
    await message.reply('Hello')


@dp.message(Command('edit'))
async def info(message: types.Message):
    btn_yt = KeyboardButton(text='YouTube', url='https://youtube.com')
    btn_rt = KeyboardButton(text='RuTube', url='https://rutube.ru')
    markup = ReplyKeyboardMarkup(keyboard=[[btn_yt, btn_rt]],
                                 one_time_keyboard=True)
    await message.reply('buttons', reply_markup=markup)
    


async def main() -> None:
    bot = Bot(token)
    await dp.start_polling(bot)

asyncio.run(main())


# import asyncio
# import logging
# import sys
# from os import getenv

# from aiogram import Bot, Dispatcher, html
# from aiogram.client.default import DefaultBotProperties
# from aiogram.enums import ParseMode
# from aiogram.filters import CommandStart
# from aiogram.types import Message

# # Bot token can be obtained via https://t.me/BotFather
# TOKEN = getenv("BOT_TOKEN")

# # All handlers should be attached to the Router (or Dispatcher)

# dp = Dispatcher()


# @dp.message(CommandStart())
# async def command_start_handler(message: Message) -> None:
#     """
#     This handler receives messages with `/start` command
#     """
#     # Most event objects have aliases for API methods that can be called in events' context
#     # For example if you want to answer to incoming message you can use `message.answer(...)` alias
#     # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
#     # method automatically or call API method directly via
#     # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
#     await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")


# @dp.message()
# async def echo_handler(message: Message) -> None:
#     """
#     Handler will forward receive a message back to the sender

#     By default, message handler will handle all message types (like a text, photo, sticker etc.)
#     """
#     try:
#         # Send a copy of the received message
#         await message.send_copy(chat_id=message.chat.id)
#     except TypeError:
#         # But not all the types is supported to be copied so need to handle it
#         await message.answer("Nice try!")


# async def main() -> None:
#     # Initialize Bot instance with default bot properties which will be passed to all API calls
#     bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # And the run events dispatching
#     await dp.start_polling(bot)


# if __name__ == "__main__":
#     logging.basicConfig(level=logging.INFO, stream=sys.stdout)
#     asyncio.run(main())
