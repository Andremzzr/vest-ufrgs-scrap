import requests
import time

MAX_RETRIES = 5

def get_data(url, form_data, retries=MAX_RETRIES, backoff_factor=4):
    for attempt in range(retries):
        try:
            response = requests.post(url, data=form_data, timeout=10)
            if response.status_code == 200:
                return response
            else:
                print(f"Attempt {attempt+1}/{retries}: Received status {response.status_code}. Retrying...")
        except requests.RequestException as e:
            print(f"Attempt {attempt+1}/{retries}: Request failed due to {e}. Retrying...")

        time.sleep(backoff_factor ** attempt)  

    return None 
 