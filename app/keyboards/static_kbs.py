from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from bot import orders_spreadsheet


# reply keyboard buttons text
i_am_admin_btn_text = "Я админ 😎"
drink_order_btn_text = "Выбрать ☕️"
profile_btn_text = "Профиль 👤"

# inline keyboard buttons callback data
add_order_manually_btn_cb = "add_order_manually"
confirm_btn_cb = "confirm"
reject_btn_cb = "reject"

# main menu keyboard
menu_btn = KeyboardButton(text=drink_order_btn_text)
profile_btn = KeyboardButton(text=profile_btn_text)
i_am_admin_btn = KeyboardButton(text=i_am_admin_btn_text)
main_kb = ReplyKeyboardMarkup(
    keyboard=[[menu_btn], [profile_btn]], resize_keyboard=True
)
admins_main_kb = ReplyKeyboardMarkup(
    keyboard=[[menu_btn], [profile_btn], [i_am_admin_btn]],
    resize_keyboard=True,
)

# bio keyboard
edit_name_cb = "edit_name"
add_training_result_cb = "add_training_result"
bio_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Редактировать никнейм", callback_data=edit_name_cb
            )
        ]
        #                       ,
        # [InlineKeyboardButton(text='Добавить тренировку',
        #                       callback_data=add_training_result_cb)]
    ]
)

# admin inline keyboard
add_order_btn = InlineKeyboardButton(
    text="✍🏼 Добавить заказ вручную", callback_data=add_order_manually_btn_cb
)
open_table_btn = InlineKeyboardButton(
    text="📄 Открыть таблицу", url=orders_spreadsheet.url
)
admin_inline_kb = InlineKeyboardMarkup(
    inline_keyboard=[[add_order_btn], [open_table_btn]]
)

# confiramtion keyboard
no_btn = InlineKeyboardButton(text="❌", callback_data=reject_btn_cb)
yes_btn = InlineKeyboardButton(text="✅", callback_data=confirm_btn_cb)
confirmation_kb = InlineKeyboardMarkup(inline_keyboard=[[no_btn, yes_btn]])

github_url = "https://github.com/enikeevtg/SkuRunCoffeeBot"
github_kb = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="GitHub", url=github_url)]]
)

# redirection keyboard
redirection_btn = InlineKeyboardButton(
    text="Записаться", callback_data="redirect"
)
redirection_kb = InlineKeyboardMarkup(inline_keyboard=[[redirection_btn]])
