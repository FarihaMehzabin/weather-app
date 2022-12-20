# from threading import Thread
# import time
# import requests


# arr = ['london', 'london', 'New York', 'New York']

# def run_request(src):
#     requests.get(
#             f"http://127.0.0.1:8080?city={src}"
#         )

# for x in range(4):
#     t = Thread(target=run_request, args=('london'))
#     t.daemon = True
#     t.start()

# time.sleep(10)


import concurrent.futures
import time
import requests

arr = ['london', 'london', 'New York', 'New York']
# arr = ['london', 'New York', 'london', 'New York']
# arr = ['london', 'New York', 'Berlin', 'Dubai']
THREAD_POOL = 5


def run_request(src):
    requests.get(
            f"http://127.0.0.1:8080?city={src}"
        )


with concurrent.futures.ThreadPoolExecutor(max_workers=THREAD_POOL) as executor:
    executor.map(run_request, arr)