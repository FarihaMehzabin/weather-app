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
        self.admin_pass = Db.get_admin_password()
    
    def hash_password(self, password):
        hashed = hashlib.sha256(password.encode('utf-8')).hexdigest()
        
        print(hashed)
        
        self.db.add_to_config("admin_password", hashed)
    
    
    def compare_password(self, password):
        
        hashed = hashlib.sha256(password.encode('utf-8')).hexdigest()
        
        print(hashed)
        
        if hashed == self.admin_pass:
            return True
        
        return False
        