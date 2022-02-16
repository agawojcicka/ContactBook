import SQLite
from book_functions import initiate

SQLite.create_table()
SQLite.create_address_table()
SQLite.create_phone_table()

initiate()
SQLite.conn.close()

