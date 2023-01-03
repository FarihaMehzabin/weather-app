import os
from dotenv import load_dotenv
from db_functions import Db
import mysql.connector
import hashlib

load_dotenv()

GUID = os.getenv('GUID')

class Hashing:
    def __init__(self):
        self.db = Db()
    
    def hash_password(self, password):
        hashed = hashlib.sha256(password.encode('utf-8')).hexdigest()
        
        print(hashed)
        
        self.db.add_to_config("admin_password", hashed)
    
    def compare_password(self, password):
        db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password",
  database='weather_app'
)

        cursor = db.cursor()

        cursor.execute("SELECT value FROM config WHERE key_name = 'admin_password'")

        data = cursor.fetchone()
        
        if password == data[0]:
            return True
        
        return False
        