from datetime import datetime
import threading

class CityLock:
    
    def __init__(self):
        self.cities = dict()
        self.lock = threading.Lock()
    
    def log(self, message):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] | Thread ID: {threading.get_ident()} | **Inside CityLock** {message}")    
        
    def get_city_lock(self, city):
        
        self.log(f"Looking for {city} in lock_dict")
        
        if(city not in self.cities.keys()):
                
                self.log(f"{city} not found in lock_dict")
                
                self.log(f"🟠Locking, getting city lock for {city}..")
                
                self.lock.acquire()
                
                self.log(f"2nd time checking for {city} in lock_dict")
                
                if city in self.cities.keys():
                    self.lock.release()
                    self.log("2nd check successful and releasing city lock")
                    
                    return self.cities[city.lower()]
                
                self.log("adding city lock to lock_dict and releasing lock")
                
                self.cities[city.lower()] = threading.Lock()
                
                self.lock.release()
                
                return self.cities[city.lower()]
        else:
            # self.cities[city.lower()]['lock'].acquire()
            
            
            
            self.log(f"Checked in lock_dict and found {city}")
            
            return self.cities[city.lower()]
            
