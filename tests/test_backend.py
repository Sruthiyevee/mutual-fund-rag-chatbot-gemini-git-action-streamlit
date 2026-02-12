import requests
import json
import time

def test_chat():
    url = "http://127.0.0.1:8000/chat"
    headers = {"Content-Type": "application/json"}
    data = {
        "message": "What is the investment objective of HDFC Large Cap Fund?",
        "session_id": "test-session-1"
    }
    
    # Wait for server to start
    max_retries = 10
    for i in range(max_retries):
        try:
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:
                print("Success!")
                print(json.dumps(response.json(), indent=2))
                return
            else:
                print(f"Failed with status: {response.status_code}")
                print(response.text)
                return
        except requests.exceptions.ConnectionError:
            print(f"Connection failed, retrying ({i+1}/{max_retries})...")
            time.sleep(2)
            
    print("Could not connect to server.")

if __name__ == "__main__":
    test_chat()
