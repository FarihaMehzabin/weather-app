import threading

class CityLock:
    
    def __init__(self):
        self.cities = dict()
        
    def get_city_lock(self, city):
        if(city not in self.cities.keys()):
                self.cities[city.lower()] = {'lock': threading.Lock()}
        return self.cities[city.lower()]