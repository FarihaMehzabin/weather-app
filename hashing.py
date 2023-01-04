import os
from dotenv import load_dotenv
from db_functions import Db
import mysql.connector
import hashlib

load_dotenv()

GUID = os.getenv('GUID')

class Hashing:
    def __init__(self, admin_password):
        self.db = Db()
        self.admin_pass = admin_password
    
    def hash_password(self, password):
        hashed = hashlib.sha256(password.encode('utf-8')).hexdigest()
        
        print(hashed)
        
        self.db.add_to_config("admin_password", hashed)
    
    def get_admin_password(self):
        db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password",
  database='weather_app'
)

        cursor = db.cursor()

        cursor.execute("SELECT value FROM config WHERE key_name = 'admin_password'")

        data = cursor.fetchone()
        
        return data[0]
    
    def compare_password(self, password):
        
        hashed = hashlib.sha256(password.encode('utf-8')).hexdigest()
        
        print(hashed)
        
        if hashed == self.admin_pass:
            return True
        
        return False
        