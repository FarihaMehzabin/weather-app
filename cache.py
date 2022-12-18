import time
import requests
import threading
from datetime import datetime
from weather_data import WeatherData
from rate_limiter_for_Ip import Limiter
from CityLock import CityLock

class CacheByMe:
    
    def __init__(self):
        self.data = dict()
        self.lock = threading.Condition()
        self.city_lock = CityLock()
    
    def log(self, message):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] | Thread ID: {threading.get_ident()} {message}")    
        
    def get_weather_data(self, city):
        
        cache_data = self.return_cache_data(city.lower())
        if cache_data:
            return cache_data
        
        self.log(f"🌞trying to dump {city} in lock dict...")

        self.log(f"nothing in cache for {city}")
                
        lock_city_up = self.city_lock.get_city_lock(city)
        
        
        if lock_city_up is not None:

            self.log(f"❌ Locking begins... for {city}. Locked status: {lock_city_up['lock'].locked()} ")
            lock_city_up['lock'].acquire()
            # while True:
                
            cache_data = self.return_cache_data(city.lower())
            if cache_data:
                lock_city_up['lock'].release()
                return cache_data
                
                
        self.log(f'😭trying to fetch weather for {city}')
        
        response = requests.get(
                        f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid=106c8085ba2b900cce93846e18cedece"
                    )
        
        self.log(f'🙌 Done fetching weather for {city} ')

        self.log("Start sleep for 10s")
        time.sleep(10)
        self.log("End sleep for 10s")
            
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
            
        # self.lock.acquire()
        self.log(f"Adding to cache..for {city}")
        
        self.add_weather_data(weather_data.city.lower(), weather_data)
        
        # self.lock.release()
        lock_city_up['lock'].release()
        
        data = WeatherData.create_weather_json(weather_data)
        
        data.headers.add('Access-Control-Allow-Origin', '*')
           
        return data        
    
    
    def check_cache_expiry(self, city):
        # check if city exists
        cache_data = self.data
        if city.lower() not in self.data.keys(): return False
        
        time_passed = time.time() - self.data[city]['time_set']
        if time_passed>=600:
            del cache_data[city.lower()]
            # del self.lock_dict[city.lower()]
            return False   
        else:
            return self.data[city]['value']
        
    
    def add_weather_data(self,city, weather_data):
        self.data[city.lower()] = {'value': weather_data, 'time_set': time.time()}
        
    
    def return_cache_data(self, city):
        cache_check = self.check_cache_expiry(city.lower())
        
        if cache_check:
            self.log(f"🖨️ Printed from cache for {city} ")
            cache_data = WeatherData.create_weather_json(cache_check)
            cache_data.headers.add('Access-Control-Allow-Origin', '*')
            return cache_data  
        else :
            return False
        
   
            