# Функции работы с БД SQLite3

from aiogram import Router


import sqlite3
from db_handler import db_queries
from decouple import config


class Person:
    'Person data model'
    def __init__(
        self,
        user_id,
        username,
        first_name,
        last_name,
        cup_name
    ) -> None:
        self.user_id = user_id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.cup_name = cup_name

    def __repr__(self):
        return f'''\
   user_id: {self.user_id}
  username: {self.username}
first_name: {self.first_name}
 last_name: {self.last_name}
  cup_name: {self.cup_name}
'''

    def get_person_data(self) -> tuple:
        return (self.user_id,
                self.username,
                self.first_name,
                self.last_name,
                self.cup_name)


def person_table_check():
    try:
        fp = open(config('DB_FILE'), 'r')
        fp.close()
    except:
        create_person_table()


def db_connection():
    connection = sqlite3.connect(config('DB_FILE'))
    cursor = connection.cursor()
    return connection, cursor


def db_closing(connection, cursor):
    cursor.close()
    connection.close()


def create_person_table():
    connection, cursor = db_connection()
    cursor.execute(db_queries.q_create_person_table)
    connection.commit()
    db_closing(connection, cursor)  


def insert_user_to_person_table(user: Person):
    person_table_check()
    connection, cursor = db_connection()
    cursor.execute(db_queries.q_create_person_table)
    cursor.execute(db_queries.q_insert_user_to_person_table,
                   user.get_person_data()
                  )
    connection.commit()
    db_closing(connection, cursor)


def select_user_from_person_table(user_id: int) -> tuple:
    person_table_check()
    connection, cursor = db_connection()
    cursor.execute(db_queries.q_check_user_in_person_table, (user_id,))
    user = cursor.fetchall()
    db_closing(connection, cursor)
    return user[0] if len(user) > 0 else None


def get_cup_name_from_person_table(user_id: int):
    user = select_user_from_person_table(user_id)
    return user[5] if user != None else None


def update_cup_name_in_person_table(user_id: int, cup_name: str):
    person_table_check()
    connection, cursor = db_connection()
    cursor.execute(db_queries.q_update_user_in_person_table,
                   (cup_name,
                    user_id)
                  )
    connection.commit()
    db_closing(connection, cursor)
