from functools import cache
from flask import Flask, request, jsonify, render_template
import json
import time
import requests
import threading
from cache import CacheByMe
from weather_data import WeatherData
from rate_limiter_for_Ip import Limiter
from ModifyDict import ModifyDict
from db_functions import Db
from views import Views


config = {
    "DEBUG": True,  # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300,
}


app = Flask(__name__)
# CORS(app)

    

# public class instances 
limiter = Limiter()
cache_instance = CacheByMe()
lock = threading.Lock()
db = Db()
view = Views()


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
            
        
        return cache_instance.get_weather_data(source.lower())
    

    except Exception as err:
        print(f"{err}")
        return jsonify(error="Something went wrong :(")


@app.route("/logs/ua")
def user_list():
    return view.return_user_agent_list()


@app.route("/logs/log")
def log_list():
    return view.return_log_list()


app.run(host="0.0.0.0", port=8080)


# @app.errorhandler(500)
# def internal_error(error):
#     return jsonify(
#         message = "Error occurred"
#         ), 500


# @app.errorhandler(404)
# def internal_error(error):
#     return jsonify(
#         message = "Error occurred"
#         ), 404


# print(f"date is {datetime.now().strftime('%H:%M:%S')} and {res['name']}")


# now = datetime.now()

# current_time = now.strftime("%H:%M:%S")
# print("Current Time =", current_time)



# class TimeoutVar:
#     """Variable whose values time out."""

#     def __init__(self, value, timeout):
#         """Store the timeout and value."""
#         self._value = value
#         self._last_set = time.time()
#         self.timeout = timeout

#     @property
#     def value(self):
#         """Get the value if the value hasn't timed out."""
#         if time.time() - self._last_set < self.timeout:
#             return self._value