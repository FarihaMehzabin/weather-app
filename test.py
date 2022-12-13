from email import message
from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
import json
from flask_caching import Cache
from datetime import datetime, timedelta
import time


config = {
    "DEBUG": True,  # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300,
}


app = Flask(__name__)
CORS(app)


# Flask-Caching setup
app.config.from_mapping(config)
cache = Cache(app)


# classes
''' Creating an object with the fetched data'''
class WeatherData:
    def __init__(
        self,
        place,
        forecast,
        time_updated,
        next_time_updated,
        temp,
        feels_like,
        humidity,
    ):
        self.city = place
        self.weatherForecast = forecast
        self.time_updated = time_updated
        self.next_time_updated = next_time_updated
        self.humidityVal = humidity
        self.temperature = temp
        self.feels_likeVal = feels_like
        
    def create_weather_json(data):
        return jsonify(
        name=data.city,
        weather=data.weatherForecast,
        temp=data.temperature,
        feels_like=data.feels_likeVal,
        humidity=data.humidityVal,
        time_refreshed=data.time_updated,
        next_refresh=data.next_time_updated,
    )
        
class ip_addr_data:
    ip_list = []
    
    def check_for_ip(ip):
        data = ip_addr_data.ip_list
        for i in range(len(data)):
            if(data[i]['addr']== ip and int(time.time()) - data[i]['time'] > 10):
                return {
                    'index': i, 
                    'delete': True,
                }
            elif(data[i]['addr']== ip and int(time.time()) - data[i]['time'] <= 10):
                return{
                    'delete': False,
                }

# ip_addr_list = []

<<<<<<< HEAD
=======

            

>>>>>>> 2cd60c2a2a7255ecfac1aef1006d406f1cfbbad1

@app.route("/", methods=["GET"])
def index():
    try:
        ip_addr = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
        
        rate_limit = ip_addr_data.check_for_ip(str(ip_addr))
        
        # print(ip_addr_list, rate_limit)
        
        ip_addr_list = ip_addr_data.ip_list
        
        if rate_limit is None:
            ip_addr_list.append({'addr': f"{ip_addr}", 'time': int(time.time())})
        
        if rate_limit is not None and rate_limit["delete"]:
            del ip_addr_list[rate_limit['index']]
            ip_addr_list.append({'addr': f"{ip_addr}", 'time': int(time.time())})
            
        elif rate_limit is not None and rate_limit["delete"] == False:
            return jsonify(rate_limit_response="rate limit reached. Please try again in 10 seconds.")
            
        source = request.args.get(
            "city"
        )  # getting parameters from url. Whatever comes after ? is a parameter

        # checking if exists in cache
        cache_check = cache.get(source.lower())
        if cache_check is not None:
            return WeatherData.create_weather_json(cache_check)

        # fetching weather using city name
        response = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={source}&units=metric&appid=106c8085ba2b900cce93846e18cedece"
        )
        res = response.json()

        # setting up data
        weatherData = WeatherData(
            res["name"],
            res["weather"][0]["description"],
            str(time.time()),
            str(time.time()+(60*10)),
            res["main"]["temp"],
            res["main"]["feels_like"],
            res["main"]["humidity"],
        )

        # saving in cache for 10mins
        cache.set(f"{weatherData.city.lower()}", weatherData, timeout=600)

        # returning json to fetch
        return WeatherData.create_weather_json(weatherData)

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