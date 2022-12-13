import time

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