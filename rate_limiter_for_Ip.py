from datetime import datetime
import time
from flask import jsonify
import threading
from collections import Counter


class Limiter:
    # ip_list = []

    def __init__(self):
        self.ip_list = []
        self.lock = threading.Lock()
        self.counter = 0
        self.ip_list_for_counter = []
        
    def log(self, message):

        log_txt = f"[{datetime.now().strftime('%H:%M:%S')}] | Thread ID: {threading.get_ident()} {message}"

        print(log_txt)
    
    
    def check_if_limited(self, ip):
        data = self.ip_list
        
        index = self._check_if_ip_exists(ip)

        if index:
            
            self.lock.acquire()
                    
            if int(time.time()) - data[index]["time"] <= 10 and self.counter[ip]<=5:
                    
                    self.lock.release()
                    
                    return False
            
            self._apply_rate_limiter(index, ip)
            
            self.lock.release()
            
            return True 
            
        else:
            
            self._add_ip(ip)
    
    def _check_if_ip_exists(self, ip):
        
        data = self.ip_list
        
        self.lock.acquire()
        
        for i in range(len(data)):
            
            if data[i]["addr"] == ip:
                
                self.ip_list_for_counter.append(ip)
        
                self.counter = Counter(self.ip_list_for_counter)
                
                self.lock.release()
                
                return i
            
        self.lock.release()
        
        return False


    def _add_ip(self, ip):
        ip_addr_list = self.ip_list
        
        self.lock.acquire()

        ip_addr_list.append({"addr": f"{ip}", "time": int(time.time())})
        
        self.ip_list_for_counter.append(ip)
        
        self.counter = Counter(self.ip_list_for_counter)
        
        self.lock.release()

    def _apply_rate_limiter(self, index, ip_addr):
        ip_addr_list = self.ip_list
        
        self.lock.acquire()

        del ip_addr_list[index]
        
        ip_addr_list.append({"addr": f"{ip_addr}", "time": int(time.time())})
        
        del self.counter[ip_addr]
        
        self.lock.release()
        
    def return_rate_limiter():
        
        limiter_data = jsonify(rate_limit_response="rate limit reached. Please try again in 10 seconds.")
            
        limiter_data.headers.add('Access-Control-Allow-Origin', '*')
            
        return limiter_data
