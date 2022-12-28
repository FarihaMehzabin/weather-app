from db_functions import Db
from aes_encryption import Encrypt

database = Db()
encrypt = Encrypt()

database.create_db('weather_app')

database.create_table('log_message', 'log VARCHAR(255)')
database.create_table('user_info', 'user_agent VARCHAR(255), ip_address VARCHAR(255)')
database.create_table('config', 'value VARCHAR(255)', 'key_name VARCHAR(255)' )

encrypt.encrypt_api_key("106c8085ba2b900cce93846e18cedece")

# import mysql.connector

# db = mysql.connector.connect(
#   host="localhost",
#   user="root",
#   password="password",
#   database="weather_app"
# )

# cursor = db.cursor()

# sql = "DELETE FROM config WHERE key_name = 'Weather_API_Key'"

# cursor.execute(sql)

# db.commit()

# print(cursor.rowcount, "record(s) deleted")

# cursor.close()
# db.close()
