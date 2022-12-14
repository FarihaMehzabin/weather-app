from email import message
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import time
import requests
from cache import CacheByMe
from weather_data import WeatherData
from rate_limiter_for_Ip import IpAddrData


config = {
    "DEBUG": True,  # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300,
}


app = Flask(__name__)
CORS(app)

    

# public class instances 
ip_instance = IpAddrData()
cache_instance = CacheByMe()


@app.route("/", methods=["GET"])
def index():
    try:
        ip_addr = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
        
        
        ip_exists = ip_instance.check_if_ip_exists(ip_addr)
        
        if(ip_exists):
            index, is_ip_limited = ip_instance.check_if_limited(ip_addr)
            if(is_ip_limited):
                return jsonify(rate_limit_response="rate limit reached. Please try again in 10 seconds.")
            else:
                ip_instance.apply_rate_limiter(index, ip_addr)
            
        else:
            ip_instance.add_ip(ip_addr)
        
        
        source = request.args.get(
            "city"
        )  # getting parameters from url. Whatever comes after ? is a parameter
        
        # checking if exists in cache
        cache_check = cache_instance.check_in_cache(source.lower())
        
        
        if cache_check == False:
            del cache_instance.data[source.lower()]
        elif cache_check != 'Not found':
            return WeatherData.create_weather_json(cache_check)
        
        
        # fetching weather using city name
        response = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={source}&units=metric&appid=106c8085ba2b900cce93846e18cedece"
        )
        res = response.json()

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
        
        print(cache_instance.data)
        # returning json to fetch
        return WeatherData.create_weather_json(weather_data)

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