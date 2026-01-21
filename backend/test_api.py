import requests
import json

url = "http://127.0.0.1:8000/chat"
headers = {"Content-Type": "application/json"}
data = {
    "message": "I want to go to Paris",
    "state": {}
}

try:
    response = requests.post(url, headers=headers, json=data)
    print("Status Code:", response.status_code)
    print("Response JSON:", json.dumps(response.json(), indent=2))
except Exception as e:
    print("Error:", e)
