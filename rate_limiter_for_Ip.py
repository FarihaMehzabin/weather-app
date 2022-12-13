import time
from flask import jsonify

class IpAddrData:
    # ip_list = []
    
    def __init__(self):
        self.ip_list = []
    
    def check_for_ip(self, ip):
        data = self.ip_list
        for i in range(len(data)):
            if(data[i]['addr']== ip and int(time.time()) - data[i]['time'] > 10):
                return i, True, 'Found'
            elif(data[i]['addr']== ip and int(time.time()) - data[i]['time'] <= 10):
                return i, False, 'Found'
        
        return 0, True, "not found"
                
    def apply_rate_limiter(self, index, delete, found, ip_addr):
        ip_addr_list = self.ip_list
            
        if found == 'not found':
            ip_addr_list.append({'addr': f"{ip_addr}", 'time': int(time.time())})
            
        elif delete == True:
            del ip_addr_list[index]
            ip_addr_list.append({'addr': f"{ip_addr}", 'time': int(time.time())})
                
        elif delete == False:
            return jsonify(rate_limit_response="rate limit reached. Please try again in 10 seconds.")