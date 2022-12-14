import time
from flask import jsonify

class Limiter:
    # ip_list = []
    
    def __init__(self):
        self.ip_list = []
    
    def check_if_ip_exists(self, ip):
        data = self.ip_list
        for i in range(len(data)):
            if (data[i]['addr']== ip):
                return True
                
        return False
    
    def check_if_limited(self, ip):
        data = self.ip_list
        for i in range(len(data)):
            if(data[i]['addr']== ip and int(time.time()) - data[i]['time'] > 10):
                return i, False
            elif(data[i]['addr']== ip and int(time.time()) - data[i]['time'] <= 10):
                return -1, True
    
    def add_ip(self, ip):
        ip_addr_list = self.ip_list
        
        ip_addr_list.append({'addr': f"{ip}", 'time': int(time.time())})

                
    def apply_rate_limiter(self, index, ip_addr):
        ip_addr_list = self.ip_list
                        
        del ip_addr_list[index]
        ip_addr_list.append({'addr': f"{ip_addr}", 'time': int(time.time())})
                
