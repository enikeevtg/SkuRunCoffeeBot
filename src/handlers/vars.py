# Некоторые переменные для обработчиков команд

from decouple import config


# handlers.menu
order_id = int(config('FIRST_ORDER_ROW'))

# handlers.menu
# Временная база заказов в текущий день
# {user_id: {
#            'name': 'Тагир',
#            'drink': 'Шиповник'
#           }
# }
orders = {}

# handlers.menu
# КАТЕГОРИИ И ПОДКАТЕГОРИИ НАПИТКОВ
drink_names = ['Американо', 'Шиповник', 'Фильтр-кофе']
amerincano_options = ['Американо', 'Американо со сливками',
                      'Американо с овсяным молоком']
rosehip_options = ['Шиповник', 'Шиповник с мёдом', 'Шиповник со льдом',
                   'Шиповник с мёдом и льдом']

# amerincano_options = ['Сливки', 'Овсяное молоко 🥛',
#                       'Просто американо, пожалуйста ☕️']
# rosehip_options = ['Лёд 🧊', 'Мёд 🍯', 'Всего и побольше 😋 🧊 🍯',
#                    'Просто шип, пожалуйста']
