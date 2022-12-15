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
        
        lock = threading.Lock()
        
        # if(limiter.check_if_limited(ip_addr)):
        #     limiter_data = jsonify(rate_limit_response="rate limit reached. Please try again in 10 seconds.")
        #     limiter_data.headers.add('Access-Control-Allow-Origin', '*')
        #     return limiter_data
        
        
        source = request.args.get(
            "city"
        )  # getting parameters from url. Whatever comes after ? is a parameter
        
        
        lock.acquire()
        print(source)
        print(f'{time.time()} Off to fetch weather and locking {lock.locked()}')

        
        # checking if exists in cache
        cache_check = cache_instance.check_in_cache(source.lower())
        if cache_check:
            print(f"I'm from cache {lock.locked()}")
            cache_data = WeatherData.create_weather_json(cache_check)
            cache_data.headers.add('Access-Control-Allow-Origin', '*')
            return cache_data
        
        
        # fetching weather using city name
        response = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={source}&units=metric&appid=106c8085ba2b900cce93846e18cedece"
        )
        time.sleep(10)
        print(f"getting weather for {source}")
        res = response.json()
        
        
        # print(res.headers())
        # setting up data
        weather_data = WeatherData(
            res["name"],
            res["weather"][0]["description"],
            str(time.time()),
            str(time.time()+(60*10)),
            res["main"]["temp"],
            res["main"]["feels_like"],
            res["main"]["humidity"],
        )
    
        # saving in cache for 10mins
        cache_instance.add_weather_data(weather_data.city.lower(), weather_data)
        
        lock.release()
        print(f'{time.time()} Done fetching weather and unlocking {lock.locked()}')

       
        print(cache_instance.data)
        # returning json to fetch
        data = WeatherData.create_weather_json(weather_data)
        data.headers.add('Access-Control-Allow-Origin', '*')
        return data
    

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