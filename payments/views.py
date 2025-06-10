from django.shortcuts import render
import requests, json, base64
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

consumer_key = 'ZQaaC5FfdMwbIevdjhh6ckkV1G93wnqeCIpqyj6awevHKQOo'
consumer_secret = 'HSeR0wNt5e5YxjSin3grKREeHjIQ4xZp7epJT6U5JpJK4e0YQUdj9po9jjxlEwdH'
shortcode = 'YOUR_SHORTCODE'
passkey = 'YOUR_PASSKEY'

def get_access_token():
    url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    response = requests.get(url, auth=(consumer_key, consumer_secret))
    return response.json()['access_token']

@csrf_exempt
def stk_push(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        phone = data['phone']
        amount = data['amount']
        description = data['description']

        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        password = base64.b64encode((shortcode + passkey + timestamp).encode()).decode()
        access_token = get_access_token()

        payload = {
            "BusinessShortCode": shortcode,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": shortcode,
            "PhoneNumber": phone,
            "CallBackURL": "https://example.com/callback/",
            "AccountReference": "WiFi Payment",
            "TransactionDesc": description
        }

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        response = requests.post(
            "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest",
            json=payload,
            headers=headers
        )

        return JsonResponse(response.json())
