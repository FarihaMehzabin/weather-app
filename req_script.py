# from threading import Thread
# import time
# import requests
# import traceback

# try:
#     def run_request():
#         requests.get(
#                 url = f"https://localhost:8080?city=london", verify='cert.pem'
#             )

#     for x in range(4):
#         t = Thread(target=run_request)
#         t.daemon = True
#         t.start()

#     time.sleep(10)

# except Exception as err:
#         print(traceback.format_exc())
#         print(f"{err}")


import concurrent.futures
import time
import requests

arr = ['london', 'london', 'New York', 'New York']
# arr = ['london', 'New York', 'london', 'New York']
# arr = ['london', 'New York', 'Berlin', 'Dubai']
THREAD_POOL = 5

print("Running")

def run_request(src):
    requests.get(
           url = f"https://127.0.0.1:8080?city={src}", verify=False
        )

with concurrent.futures.ThreadPoolExecutor(max_workers=THREAD_POOL) as executor:
    executor.map(run_request, arr)