# Набор запросов в БД SQLite3


q_create_person_table = \
  'CREATE TABLE IF NOT EXISTS person ( \
      id INTEGER PRIMARY KEY, \
      user_id INTEGER, \
      username VARCHAR (21), \
      first_name VARCHAR (21), \
      last_name VARCHAR (21), \
      cup_name VARCHAR (21) \
  )'


q_insert_user_to_person_table = \
  'INSERT INTO person (user_id, username, first_name, last_name, cup_name) \
   VALUES (?, ?, ?, ?, ?)'


q_check_user_in_person_table = \
  'SELECT * FROM person WHERE user_id = ?'


q_update_user_in_person_table = \
  'UPDATE person \
   SET cup_name = ? \
   WHERE user_id = ?'
