from functools import cache
from os import abort
from flask import Flask, request, jsonify, render_template
import json
import time
import requests
import traceback
import threading
from cache import Cache
from weather_data import WeatherData
from rate_limiter_for_Ip import Limiter
from ModifyDict import ModifyDict
from db_functions import Db
from views import Views
from aes_encryption import Encrypt
from hashing import Hashing


config = {
    "DEBUG": True,  # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300,
}


app = Flask(__name__)



# public class instances 
limiter = Limiter()
lock = threading.Lock()
db = Db()
view = Views()
encrpt = Encrypt()
api_key = encrpt.get_api_key()
admin_password = encrpt.get_admin_password()
cache_instance = Cache(api_key)
hashing = Hashing(admin_password)


@app.route("/", methods=["GET"])
def index():
    try:
        ip_addr = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
        
        source = request.args.get(
            "city"
        )  
        
        db.add_user_data(request.headers.get('User-Agent'),ip_addr)
        
        if(limiter.check_if_limited(ip_addr)):
            
            return cache_instance.get_weather_data(source.lower(), True)
            
        else:
            
            return cache_instance.get_weather_data(source.lower())
    

    except Exception as err:
        print(traceback.format_exc())
        print(f"{err}")
        return jsonify(error="Something went wrong :(")


@app.route("/logs/ua")
def user_list():
    return view.return_user_agent_list()


@app.route("/logs/log", methods=["GET"])
def log_list():
    
    password = request.args.get(
            "password"
        ) 
    
    if hashing.compare_password(password):
        return view.return_log_list()
    
    return "", 403
    
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, ssl_context=('cert.pem', 'key.pem'))
