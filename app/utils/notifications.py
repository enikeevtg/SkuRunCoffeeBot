from bot import admins_ids, bot, group_id
from database import requests as rq
from keyboards import admins_kb, redirection_kb
from handlers.messages import group_morning_notification


async def send_admins_bot_start_notification():
    for admin_id in admins_ids:
        nickname = await rq.get_nickname(admin_id)
        await bot.send_message(admin_id, nickname + ', я проснулся 🤗\n',
                               reply_markup=admins_kb)


async def send_group_bot_start_notification():
    await bot.send_message(chat_id=group_id,
                           text=group_morning_notification,
                           reply_markup=redirection_kb)
