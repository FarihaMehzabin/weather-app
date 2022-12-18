import threading

class CityLock:
    
    def __init__(self):
        self.cities = dict()
        self.lock = threading.Lock()
        
    def get_city_lock(self, city):
        
        if(city not in self.cities.keys()):
                self.lock.acquire()
                if city in self.cities.keys():
                    self.lock.release()
                    return self.cities[city.lower()]
                self.cities[city.lower()] = {'lock': threading.Lock()}
                # return self.cities[city.lower()]
                self.lock.release()
                return self.cities[city.lower()]
        else:
            # self.cities[city.lower()]['lock'].acquire()
            return self.cities[city.lower()]
            
