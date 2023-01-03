from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import os
from dotenv import load_dotenv
from db_functions import Db
import mysql.connector
import base64

load_dotenv()

AES_KEY = os.getenv('AES_KEY')

class Encrypt:
    
    def __init__(self):
        
        self.header = b"header"
        self.db = Db()
    
    def encrypt_api_key(self, api_key):
        
        encryption_cipher = AES.new(AES_KEY.encode("utf8"), AES.MODE_OPENPGP)

        ciphertext = encryption_cipher.encrypt(api_key.encode("utf8"))

        b64_ciphertext = base64.b64encode(ciphertext).decode()
        print("Base64 of AES-encrypted message: ", b64_ciphertext)
        
        self.db.add_to_config('Weather_API_Key', b64_ciphertext)
        
        
    def get_api_key(self):
        
        db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password",
  database='weather_app'
)

        cursor = db.cursor()

        cursor.execute("SELECT value FROM config WHERE key_name = 'Weather_API_Key'")

        data = cursor.fetchone()
        
        api_key = data[0]

        cursor.close()
        db.close()
        
        unb64_ciphertext = base64.b64decode(api_key.encode())
        iv = unb64_ciphertext[0:18]
        unb64_ciphertext = unb64_ciphertext[18:]

        decryption_cipher = AES.new(AES_KEY.encode("utf8"), AES.MODE_OPENPGP, iv=iv)#, nonce=nonce)
        output_data = decryption_cipher.decrypt(unb64_ciphertext)

        return output_data.decode()
        # print("Decrypted message: ", output_data.decode())


