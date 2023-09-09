import json

import requests
from requests.auth import HTTPBasicAuth

# auth data for: username and password
auth = HTTPBasicAuth('developer@bookeasyclean.com', 'operations')
data = {"username": 'developer@bookeasyclean.com', "password": 'operations'}

try:
    login_response = requests.post('https://app.bookeasyclean.com/api/v1/login', data=json.dumps(data), auth=auth)
    print(login_response.json())
    login_response_data = login_response.json()
    if login_response_data["response"]["code"] == 200 and login_response_data["response"]["message"] == 'Success':
        api_token = login_response_data["response"]["data"]["session_token"]
        print(api_token)
except Exception as e:
    api_token = ''
    print(e)
    print("Login Failed!/Something Wrong!")
