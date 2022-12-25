import mysql.connector
from flask import render_template

class Views:
    # def __init__(self):
        
        
    def return_user_agent_list(self):
        db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password",
  database='weather_app'
)

        cursor = db.cursor()

        cursor.execute("SELECT * FROM user_info ORDER BY ID DESC LIMIT 100")

        result = cursor.fetchall()

        cursor.close()
        db.close()
        
        return render_template('user_agent.html', data=result)
        
    def return_log_list(self):
        db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password",
  database='weather_app'
)

        cursor = db.cursor()

        cursor.execute("SELECT * FROM log_message ORDER BY ID DESC LIMIT 100")

        result = cursor.fetchall()

        # for x in result:
        #     print(x)

        cursor.close()
        db.close()
        
        return render_template('log.html', data=result)