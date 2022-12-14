import time

class CacheByMe:
    # data = dict()
    
    def __init__(self):
        self.data = dict()
    
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
        
   
            