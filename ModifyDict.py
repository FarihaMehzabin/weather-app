import time
import threading
from datetime import datetime

class ModifyDict:
    
    def __init__(self, dictionary):
        self.data = dictionary
        self.lock = threading.Lock()
        
    
    def log(self, message):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] | Thread ID: {threading.get_ident()} | **Inside CityLock** {message}")    
    
    def check_cache_expiry(self, city):
        # check if city exists
        cache_data = self.data
        if city.lower() not in self.data.keys(): return False
        
        time_passed = time.time() - self.data[city]['time_set']
        if time_passed>=600:
            self.lock.acquire()
            
            self.log(f"Locking and removing expired cache data")
            
            del cache_data[city.lower()]
            # del self.lock_dict[city.lower()]
            self.log("Unlocked and done removing cache data")
            self.lock.release()
            return False   
        else:
            return self.data[city]['value']
    
    
    def add_weather_data(self,city, weather_data):
        
        self.lock.acquire()
        
        self.log(f"Locking and Adding weather data for {city}")
        
        self.data[city.lower()] = {'value': weather_data, 'time_set': time.time()}
        
        self.log(f"Unlocked and added weather data for {city}")
        self.lock.release()
        
    