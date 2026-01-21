import requests
import json

def test_server():
    url = "http://127.0.0.1:8000/chat"
    headers = {'Content-Type': 'application/json'}
    payload = {
        "message": "I want to go to Athirappilly",
        "state": {}
    }
    
    print(f"Testing {url} with payload: {payload}")
    try:
        response = requests.post(url, headers=headers, json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            print("[SUCCESS] Server is reachable and responding.")
        else:
             print("[FAIL] Server returned error.")
    except Exception as e:
        print(f"[FAIL] Could not connect to server: {e}")

if __name__ == "__main__":
    test_server()
