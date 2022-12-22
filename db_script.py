from db_functions import Db

database = Db()

database.create_db('weather_app')

database.create_table('weather_app','log_message', 'log VARCHAR(255)')
database.create_table('weather_app','user_info', 'user_agent VARCHAR(255), ip_address VARCHAR(255)')

