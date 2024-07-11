# БАЗЫ ДАННЫХ:
db_file = './skurun.sql'
# временная база заказов в текущий день
# {chat_id: {
#            'name': 'Тагир',
#            'drink': 'Шиповник'
#           }
# }
orders = {}


# КОМАНДЫ
# start - начнём
# menu - выбери напиток
# name - посмотри, что мы напишем на твоём следующем стаканчике
# edit - измени имя своего стаканчика
commans_msg = 'Используй следующие доступные команды:\n' + \
              '/menu - выбери напиток из меню\n' + \
              '/name - проверь имя своего стаканчика\n' + \
              '/edit - измени имя своего стаканчика'


# ТЕКСТЫ СООБЩЕНИЙ
starting_msg = 'Рост\n' + \
               'время на 5000\n' + \
               'степень кофемании и любимый сорт напитка 😁\n' + \
               '©️ FranticDog'
# starting_animation = 'sources/starting_animation.mp4'
starting_animation = \
  r'https://cs9.pikabu.ru/post_img/2017/10/27/7/1509102404164624978.gif'
cup_name_query_msg = 'Как подписать твой стаканчик? ✍️'
order_msg = 'Записал, отправил, обнял, приподнял, поставил, жди пирогов и '

name_false_msg = 'Так... В имени должны быть только алфавитные символы ' + \
                 'без пробелов 🤨'
name_true_msg = 'Супер. Давай теперь выберем напиток!'

edit_name_msg = ', ты решил(а) изменить имя?\nНиже введи новое, ' + \
                'которое мы напишем на твоём следующем стаканчике ✍️'

choose_drink_msg = 'Выбери напиток из списка 👇\n' + \
                   'У тебя всего одна попытка'
choose_option_msg = 'Выбери вариант напитка из списка 👇'
try_again_msg = 'Упс... При заказе что-то пошло не так. Попробуй ещё раз'


# КАТЕГОРИИ И ПОДКАТЕГОРИИ НАПИТКОВ
types_of_coffee = ['Американо ☕️', 'Шиповник', 'Фильтр-кофе']
amerincano_options = ['Американо', 'Американо со сливками',
                      'Американо с овсяным молоком']
rosehip_options = ['Шиповник', 'Шиповник с мёдом', 'Шиповник со льдом',
                   'Шиповник с мёдом и льдом']

# amerincano_options = ['Сливки', 'Овсяное молоко 🥛',
#                       'Просто американо, пожалуйста ☕️']
# rosehip_options = ['Лёд 🧊', 'Мёд 🍯', 'Всего и побольше 😋 🧊 🍯',
#                    'Просто шип, пожалуйста']

