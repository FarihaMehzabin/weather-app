from datetime import datetime
import time
from flask import jsonify
import threading


class Limiter:
    # ip_list = []

    def __init__(self):
        self.ip_list = []
        self.lock = threading.Lock()
        
    def log(self, message):

        log_txt = f"[{datetime.now().strftime('%H:%M:%S')}] | Thread ID: {threading.get_ident()} {message}"

        print(log_txt)
    
    
    def check_if_limited(self, ip):
        data = self.ip_list
        
        index = self._check_if_ip_exists(ip)

        if index:
            
            self.lock.acquire()
            
            if int(time.time()) - data[index]["time"] > 10:
                
                    self._apply_rate_limiter(index, ip)
                    
                    self.lock.release()
                    
            elif int(time.time()) - data[index]["time"] <= 10:
                    
                    self.lock.release()
                    
                    return True
            
            self.lock.release()
            
        else:
            
            self._add_ip(ip)
    
    def _check_if_ip_exists(self, ip):
        
        data = self.ip_list
        
        self.lock.acquire()
        
        for i in range(len(data)):
            
            if data[i]["addr"] == ip:
                
                self.lock.release()
                
                return i
            
        self.lock.release()
        
        return False


    def _add_ip(self, ip):
        ip_addr_list = self.ip_list
        
        self.lock.acquire()

        ip_addr_list.append({"addr": f"{ip}", "time": int(time.time())})
        
        self.lock.release()

    def _apply_rate_limiter(self, index, ip_addr):
        ip_addr_list = self.ip_list
        
        self.lock.acquire()

        del ip_addr_list[index]
        
        ip_addr_list.append({"addr": f"{ip_addr}", "time": int(time.time())})
        
        self.lock.release()
        
    def return_rate_limiter(self):
        
        limiter_data = jsonify(rate_limit_response="rate limit reached. Please try again in 10 seconds.")
            
        limiter_data.headers.add('Access-Control-Allow-Origin', '*')
            
        return limiter_data
