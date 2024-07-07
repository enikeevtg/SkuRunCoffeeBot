query_create_person_table = \
  'CREATE TABLE IF NOT EXISTS person ( \
      id INTEGER PRIMARY KEY, \
      user_id INTEGER, \
      username VARCHAR (21), \
      first_name VARCHAR (21), \
      last_name VARCHAR (21), \
      cup_name VARCHAR (21) \
  )'

query_insert_user_to_person_table = \
  'INSERT INTO person (user_id, username, first_name, last_name, cup_name) \
   VALUES (?, ?, ?, ?, ?)'

query_check_user_in_table = \
  'SELECT * FROM person WHERE user_id = ?'
