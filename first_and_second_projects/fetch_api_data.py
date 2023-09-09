import requests
import json
import pandas as pd
from datetime import date, datetime
from dateutil import parser


def get_api_data(token):
    url = "https://app.bookeasyclean.com/api/v1/export-bookings"
    headers = {
        "Authorization": f"Bearer {token}",
        # "Connection": "keep-alive",
        # "Accept-Encoding": "gzip, deflate, br",
        # "Accept-Language": "en-US,en;q=0.9",
        # "Cache-Control": "no-cache",
        # "Cookie": "__stripe_mid=6af1149b-c823-4ab4-8ff8-4ce9e55fbb45b02e89; _fbp=fb.1.1686425169903.653506242; app_language=en; __stripe_sid=b5ff465e-1a22-4b3d-aed4-dc7e8f90960bebc962",
        # "Host": "app.bookeasyclean.com",
        # "Dnt": "1",
        # "Ip": "103.138.170.193", # your IP address
        # "Pragma": "no-cache",
        # "Referer": "https://app.bookeasyclean.com/admin/export/download-csv",
        # "Sec-Ch-Ua": "Not.A/Brand;v=8, Chromium;v=114, Google Chrome;v=114",
        # "Sec-Ch-Ua-Mobile": "?0",
        # "Sec-Ch-Ua-Platform": "Windows", # Windows or MacOS
        # "Sec-Fetch-Dest": "empty",
        # "Sec-Fetch-Mode": "cors",
        # "Sec-Fetch-Site": "same-origin",
        # "Accept": "application/json, text/plain, */*",
        # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }

    from_date = date.today().__str__()
    to_date = date.today().__str__()

    data = {
        "from_date": from_date,
        "to_date": to_date,
        "booking_type": "active",
        "industry_id": 0,
        "fields": {
            "booking_id": 1,
            "service_date": 1,
            "provider_name": 1,
            "discount_from_referral": 1,
            "expedited_amount": 1,
            "customer_full_name": 1,
            "service_total": 1,
            "created_by": 1,
            "transaction_id": 1,
            "price_adjustment": 1,
            "amount_paid_by_customer": 1,
            "excludes": 1,
            "job_length": 1,
            "discount_from_code": 1,
            "provider_payment_summary": 1,
            "created_on": 1,
            "customer_id": 1,
            "customer_phone": 1,
            "discount_code": 1,
            "client_id": 1,
            "giftcard_amount_used": 1,
            "booking_tax": 1,
            "price_adjustment_comment": 1,
            "frequency": 1,
            "pricing_parameter": 1,
            "customer_email": 1,
            "provider_note": 1,
            "service_fee": 1,
            "rating_comment": 1,
            "service_time": 1,
            "address": 1,
            "provider_name_without_ids": 1,
            "rating_value": 1,
            "final_amount": 1,
            "customer_last_name": 1,
            "discount_from_frequency": 1,
            "service": 1,
            "booking_note": 1,
            "amount_owed_by_customer": 1,
            "industry": 1,
            "provider_has_keys": 1,
            "customer_company_name": 1,
            "zipcode": 1,
            "customer_first_name": 1,
            "tip": 1,
            "payment_method": 1,
            "private_customer_note": 1,
            "booking_status": 1,
            "provider_payment": 1,
            "parking": 1,
            "bonus": 1,
            "extras": 1
        },
        "heading_fields": [
            "Client id",
            "Transaction id",
            "Date",
            "Time",
            "First name",
            "Last name",
            "Full name",
            "Company name",
            "Email",
            "Address",
            "Zip/Postal code",
            "Phone",
            "Rating value",
            "Rating comment",
            "Service total (USD)",
            "Sales tax",
            "Final amount (USD)",
            "Amount paid by customer (USD)",
            "Amount owed by customer (USD)",
            "Tip (USD)",
            "Parking (USD)",
            "Bonus (USD)",
            "Payment method",
            "Frequency",
            "Discount code",
            "Discount from code (USD)",
            "Discount from frequency (USD)",
            "Discount from referral (USD)",
            "Giftcard amount used (USD)",
            "Provider/team",
            "Provider/team (without ids)",
            "Provider/team payment (USD)",
            "Provider payment (summary) (USD)",
            "Provider/team has keys",
            "Created on",
            "Created by",
            "Estimated job length (HH:MM)",
            "Industry",
            "Service",
            "Booking note",
            "Private customer note",
            "Provider note",
            "Booking id",
            "Customer id",
            "Price adjustment",
            "Price adjustment comment",
            "Booking status",
            "Extras",
            "Excludes",
            "Expedited amount",
            "Service fee",
            "Pricing parameters"
        ],
        "tags": []
    }
    try:
        response = requests.post(url=url, data=json.dumps(data), headers=headers)
        if response.status_code == 200:
            dict_data = response.json()
            # print(dict_data)
            if dict_data['response']['code'] == 200:
                df = pd.read_csv(f"https://app.bookeasyclean.com{dict_data['response']['data']['upload_url']}")
                # df.to_csv(dict_data['response']['data']['upload_url'].split("/")[-1], index=False)
                return True, df
            else:
                print(response.json())
                return False, response.json()
        else:
            print(response.json())
            return False, response.json()
    except Exception as e:
        print(e)
        return False, "Something Wrong!"



'''
app.bookeasyclean.com/login

uid: developer@bookeasyclean.com
pw: operations




'''
