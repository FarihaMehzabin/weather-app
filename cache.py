import time
import requests
import threading
from datetime import datetime
from weather_data import WeatherData
from rate_limiter_for_Ip import Limiter
from CityLock import CityLock
from ModifyDict import ModifyDict
from db_functions import Db

class CacheByMe:
    def __init__(self):
        self.data = dict()
        self.lock = threading.Condition()
        self.city_lock = CityLock()
        self.modify_dict = ModifyDict(self.data)
        self.db = Db()
        self.limiter = Limiter()
    
    def log(self, message):
        
        log_txt = f"[{datetime.now().strftime('%H:%M:%S')}] | Thread ID: {threading.get_ident()} {message}"

        print(
            log_txt
        )
        
        self.db.add_log((log_txt,))

    def get_weather_data(self, city, ip_limit=False):

        cache_data = self.return_cache_data(city.lower())

        if cache_data:

            return cache_data

        self.log(f"🌞trying to dump {city} in lock dict...")

        self.log(f"nothing in cache for {city}")

        self.log(f"{city} going to CityLock class")

        lock_city_up = self.city_lock.get_city_lock(city)

        self.log(f"{lock_city_up}")

        if lock_city_up is not None:

            lock_city_up.acquire()

            self.log(
                f"❌ Locking begins... for {city}. Locked status: {lock_city_up.locked()} "
            )

        self.log(f"Second time checking in cache for {city}")
        
        cache_data = self.return_cache_data(city.lower())

        if cache_data:

            self.log(f"Second cache check successful for {city}")

            lock_city_up.release()

            return cache_data

        
        if ip_limit:
            
            self.log(f"ip is limited and data not available for {city}")

            lock_city_up.release()

            return self.limiter.return_rate_limiter()

        
        self.log(f"😭trying to fetch weather for {city}")

        response = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid=106c8085ba2b900cce93846e18cedece"
        )

        self.log(f"🙌 Done fetching weather for {city} ")

        self.log("Start sleep for 10s")

        time.sleep(10)

        self.log("End sleep for 10s")

        return self._return_weather_data(response, lock_city_up)

    def return_cache_data(self, city):
        cache_check = self.modify_dict.check_cache_expiry(city.lower())

        if cache_check:
            self.log(f"🖨️ Printed from cache for {city} ")
            cache_data = WeatherData.create_weather_json(cache_check)
            cache_data.headers.add("Access-Control-Allow-Origin", "*")
            return cache_data
        else:
            return False

    def _return_weather_data(self, response, lock):

        res = response.json()

        weather_data = WeatherData(
            res["name"],
            res["weather"][0]["description"],
            str(time.time()),
            str(time.time() + (60 * 10)),
            res["main"]["temp"],
            res["main"]["feels_like"],
            res["main"]["humidity"],
        )

        self.log(f"Adding to cache..for {res['name']}")

        self.modify_dict.add_weather_data(weather_data.city.lower(), weather_data)

        lock.release()

        weather_data = WeatherData.create_weather_json(weather_data)

        weather_data.headers.add("Access-Control-Allow-Origin", "*")

        return weather_data
