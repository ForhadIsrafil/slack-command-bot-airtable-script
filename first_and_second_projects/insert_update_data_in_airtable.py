from datetime import datetime
import json
import requests
from requests.auth import HTTPBasicAuth

import pandas as pd
from dateutil import parser
from fetch_api_data import get_api_data

table_name = "Test "
base_id = "aDyEAx"
table_id = "tblLl3Z04"
airtable_api_token = "patl83a2AzFDoie6dfbd4ba92e74c8e56b09752"

# ==========Get Bookeasyclean Token Start================
api_token = ""
try:
    auth = HTTPBasicAuth('developer@bookea.com', 'opers')
    auth_data = {"username": 'developer@bookea.com', "password": 'opers'}

    login_response = requests.post('https://app.bookeasyclean.com/api/v1/login', data=json.dumps(auth_data), auth=auth)
    # print(login_response.json())
    login_response_data = login_response.json()
    if login_response_data["response"]["code"] == 200 and login_response_data["response"]["message"] == 'Success':
        api_token = login_response_data["response"]["data"]["session_token"]
        # print(api_token)
except Exception as e:
    print(e)
    print("Login Failed!/Something Wrong!")


# ==========Get Bookeasyclean Token End================

# ========================= Don't Change below ==========================


def insert_data(all_data):
    url = f"https://api.airtable.com/v0/{base_id}/{table_id}"
    headers = {
        "Authorization": f"Bearer {airtable_api_token}",
        "Content-Type": "application/json"
    }

    response = requests.patch(url=url, data=json.dumps(all_data), headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(response.json())
        return response.json()


response_status, df = get_api_data(api_token)
# df = pd.read_csv('1686428987_bookings_2023-06-09-to-2023-06-10.csv', encoding= 'unicode_escape')
if response_status == True:
    df.fillna("", inplace=True)

    data = {"performUpsert": {"fieldsToMergeOn": ["Name", "Email", "Phone Number"]}, "typecast": True}
    fields_arr = []
    for index, single_data in df.iterrows():
        dict_data = single_data.to_dict()
        # print(dict_data)
        if dict_data['Industry'] == 'Home Cleaning':
            fields = {"fields": {
                "Name": dict_data.get("Full name", ''),
                "Date": dict_data.get("Date", ''),
                "Time": dict_data.get("Time", ''),
                "Notes": dict_data.get("Booking note", ''),
                "Provider Note": dict_data.get("Provider note", ''),
                "Service": dict_data.get("Service", ''),
                "Assignee": dict_data.get('Provider/team (without ids)', ''),
                "Status": dict_data.get('Booking status', ''),
                # "End Time": dict_data.get('Time').split(" ")[0] + " - " +
                #             dict_data.get('Estimated job length', '').split(" ")[0],
                "Length": dict_data.get('Estimated job length (HH:MM)', '').split(" ")[0],
                "Beds": dict_data.get('Bedrooms', ''),
                "Baths": dict_data.get('Bathrooms', ''),
                "Square Footage": dict_data.get('Sq ft', ''),
                "Contractor IDs": dict_data.get('Provider/team').split(":")[0],
                "Extras": dict_data.get('Extras', ''),
                "Exclusions": dict_data.get('Excludes', ''),
                "Frequency": dict_data.get('Frequency', ''),
                "Email": dict_data.get('Email', ''),
                "Phone Number": str(dict_data.get('Phone', '')),
                "Address": dict_data.get('Address', ''),
                "Apt": str(dict_data.get('Apt', '')),
                "Provider Note": dict_data.get('Provider note', ''),
                "Final Amount": dict_data.get('Final amount (USD)', ''),
                "Tip": dict_data.get('Tip (USD)', ''),
                "Sales Tax": dict_data.get('Sales tax', ''),
                "Frequency Discount Amount": dict_data.get('Discount from frequency (USD)', ''),
                "BK Customer ID": str(dict_data.get('Customer id', '')),
                "Created On (BK)": parser.parse(dict_data.get('Created on', '')).isoformat()
            }}
            fields_arr.append(fields)
            print(fields)

    data["records"] = fields_arr

    # Sending data to airtable
    print(insert_data(data))

else:
    print(response_status)

# ====================================================================================================

