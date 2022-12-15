from flask import Flask, request, jsonify
import json
import time
import requests
import threading
from cache import CacheByMe
from weather_data import WeatherData
from rate_limiter_for_Ip import Limiter


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


@app.route("/", methods=["GET"])
def index():
    try:
        ip_addr = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
        
        if(limiter.check_if_limited(ip_addr)):
            limiter_data = jsonify(rate_limit_response="rate limit reached. Please try again in 10 seconds.")
            limiter_data.headers.add('Access-Control-Allow-Origin', '*')
            return limiter_data
        
        
        source = request.args.get(
            "city"
        )  
        
        return cache_instance.get_weather_data(source.lower())
    

    except Exception as err:
        print(err)
        return jsonify(error="Something went wrong :(")


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