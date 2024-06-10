import time
import requests

URL = "https://your-render-service-url.com"

def ping_service():
    try:
        response = requests.get(URL)
        if response.status_code == 200:
            print(f"Service is up: {response.status_code}")
        else:
            print(f"Service response: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error pinging service: {e}")

while True:
    ping_service()
    time.sleep(6 * 60)