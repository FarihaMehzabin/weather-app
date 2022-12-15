import time
import requests
import threading
from datetime import datetime
from weather_data import WeatherData
from rate_limiter_for_Ip import Limiter

class CacheByMe:
    
    def __init__(self):
        self.data = dict()
        self.lock = threading.Lock()
        
        
    def get_weather_data(self, city):
        
        # self.lock.acquire()
        cache_check = self.check_in_cache(city.lower())
        
        if cache_check:
            print(f"[{datetime.now().strftime('%H:%M:%S')}]: I'm from cache")
            
            cache_data = WeatherData.create_weather_json(cache_check)
            cache_data.headers.add('Access-Control-Allow-Origin', '*')
            return cache_data
        
        # self.lock.release()
        response = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={city.lower()}&units=metric&appid=106c8085ba2b900cce93846e18cedece"
        )
        
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}]: Looking for {city} weather.")
        
        
        res = response.json()
        
        weather_data = WeatherData(
            res["name"],
            res["weather"][0]["description"],
            str(time.time()),
            str(time.time()+(60*10)),
            res["main"]["temp"],
            res["main"]["feels_like"],
            res["main"]["humidity"],
        )
        
        self.add_weather_data(weather_data.city.lower(), weather_data)
        
        data = WeatherData.create_weather_json(weather_data)
        data.headers.add('Access-Control-Allow-Origin', '*')
        
        time.sleep(10)
        print(f"[{datetime.now().strftime('%H:%M:%S')}]: slept for 10s")
        
        return data
    
    
    def check_in_cache(self, city):
        # check if city exists
        cache_data = self.data
        if city.lower() not in self.data.keys(): return False
        
        time_passed = time.time() - self.data[city]['time_set']
        if time_passed>=600:
            del cache_data[city.lower()]
            return False   
        else:
            return self.data[city]['value']
        
    def add_weather_data(self,city, weather_data):
        self.data[city.lower()] = {'value': weather_data, 'time_set': time.time()}
        
   
            