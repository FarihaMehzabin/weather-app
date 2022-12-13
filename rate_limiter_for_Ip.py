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
                return {
                    'index': i, 
                    'delete': True,
                }
            elif(data[i]['addr']== ip and int(time.time()) - data[i]['time'] <= 10):
                return{
                    'delete': False,
                }
                
    def rate_limiter(self, rate_limit, ip_addr):
        ip_addr_list = self.ip_list
            
        if rate_limit is None:
            ip_addr_list.append({'addr': f"{ip_addr}", 'time': int(time.time())})
            
        if rate_limit is not None and rate_limit["delete"]:
            del ip_addr_list[rate_limit['index']]
            ip_addr_list.append({'addr': f"{ip_addr}", 'time': int(time.time())})
                
        elif rate_limit is not None and rate_limit["delete"] == False:
            return jsonify(rate_limit_response="rate limit reached. Please try again in 10 seconds.")