import threading
import mysql.connector


class Db:
  
  
  def __init__(self):
    self.lock = threading.Lock()
  
  def create_db(self, db_name):
    
    db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password"
  )
    
    cursor = db.cursor()
    cursor.execute(f"CREATE DATABASE {db_name}")

    cursor.close()
    db.close()
  
  
  def create_table(self, table_name, columns):
    db_config = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database='weather_app'
  )
    cursor = db_config.cursor()
    cursor.execute(f"CREATE TABLE {table_name} (ID INT AUTO_INCREMENT PRIMARY KEY,{columns})")

    cursor.close()
    db_config.close()
    
  
  def add_user_data(self, *values):
    db_config = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password",
  database='weather_app'
)
    cursor = db_config.cursor()
    
    sql = f"INSERT INTO user_info (user_agent, ip_address) VALUES (%s, %s)"
    val = values
    
    cursor.execute(sql, val)

    db_config.commit()

    cursor.close()
    db_config.close()
  
  def add_log(self, *values):
    db_config = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password",
  database='weather_app'
)
    cursor = db_config.cursor()
    
    sql = f"INSERT INTO log_message (log) VALUES (%s)"
    val = values
    
    cursor.execute(sql, val)

    db_config.commit()

    cursor.close()
    db_config.close()
    
    
  