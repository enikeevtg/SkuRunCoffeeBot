# SkuRunCoffeeBot_v2

![photo](./img/IMG_7981.JPG)

Телеграм-бот для бегового клуба кофейни Скуратов в Казани.

Использована библиотека [aiogram](https://docs.aiogram.dev/en/dev-3.x/index.html).


## Команды

+ Работы с кодом ведётся из папки ./src/

      cd src

+ Подключение виртуальной среды для разработки

      make venv
      source venv/bin/activate

+ Запуск телеграм-бота:

      make run

+ Загрузка необходимых для работы бота модулей:

      make install_deps

+ Сохранение зависимостей в файл requirements.txt:

      make freeze_deps

+ Очистка проекта от файлов кеширования

      make clean


## Описание

Данные пользователей сохраняются в базе данных skurun.sql с помощью библиотеки sqlite3.

Заказы пользователей отправляются в google sheets с помощью подключения соответстующего API.
