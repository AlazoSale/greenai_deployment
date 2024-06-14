import time
import requests

URL = "https://greenai-deployment.onrender.com/api/chat/ping/"

def ping_service():
    try:
        start_time = time.time()
        response = requests.get(URL)
        end_time = time.time()
        response_time = end_time - start_time
        
        if response.status_code == 200:
            print(f"Service is up: {response.status_code}, Response time: {response_time:.2f} seconds")
        else:
            print(f"Service response: {response.status_code}, Response time: {response_time:.2f} seconds")
    except requests.exceptions.RequestException as e:
        print(f"Error pinging service: {e}")

while True:
    ping_service()
    time.sleep(0.1 * 60)  # Sleep for 3 minutes
