from db_functions import Db
from aes_encryption import Encrypt
import os
from dotenv import load_dotenv
from hashing import Hashing
import names

load_dotenv()

GUID = os.getenv('GUID')
api_key = os.getenv('API_KEY')

database = Db()
encrypt = Encrypt()
hashing = Hashing()

database.create_db('weather_app')

database.create_table('log_message', 'log VARCHAR(255)')
database.create_table('user_info', 'user_agent VARCHAR(255), ip_address VARCHAR(255)')
database.create_table('config', 'value VARCHAR(255)', 'key_name VARCHAR(255)' )

encrypt.encrypt_api_key(api_key)

hashing.hash_password(GUID)


