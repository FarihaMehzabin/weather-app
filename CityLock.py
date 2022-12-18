import threading

class CityLock:
    
    def __init__(self):
        self.cities = dict()
        self.lock = threading.Lock()
        
    def get_city_lock(self, city):
        
        if(city not in self.cities.keys()):
                self.lock.acquire()
                self.cities[city.lower()] = {'lock': threading.Lock()}
                self.lock.release()
        else:
            self.cities[city.lower()]['lock'].acquire()
            return self.cities[city.lower()]
            
