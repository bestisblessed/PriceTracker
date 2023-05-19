from flask import Flask
from flask import render_template, request
import time
import sys
import os
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from dotenv import load_dotenv
from twilio.rest import Client

## Import flask and create instance
app = Flask(__name__)
load_dotenv()

# Coinbase API endpoint to get current Bitcoin price
url = 'https://api.coinbase.com/v2/prices/BTC-USD/spot'

# To fix maximum request error
session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)
session.get(url)
#requests.get(url)

## Twilio account SID and auth token
account_sid = os.getenv('ACCOUNT_SID')
auth_token = os.getenv('AUTH_TOKEN')

## Twilio phone number and your own phone number
twilio_number = os.getenv('TWILIO_NUMBER')
your_number = os.getenv('YOUR_NUMBER')

## Variables for price threshold
#price_low = float(os.environ['PRICE_LOW'])
#price_high = float(os.environ['PRICE_HIGH'])

# Function to send a text message using Twilio
def send_message(message):
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=message,
        from_=twilio_number,
        to=your_number
    )
#    print('Message sent!')
    return 'Message sent!'

## Define routes and views: 
## Routes define the URL paths that your application will respond to. 
## Views are Python functions that handle requests and generate responses.

#@app.route('/')
#def index():
#    return 'Hello, Flask!'

#@app.route('/', methods=['GET', 'POST'])
#def index():
#    if request.method == 'POST':
#        price_low = float(request.form['price_low'])
#        price_high = float(request.form['price_high'])
#        return render_template('index.html', price_low=price_low, price_high=price_high)
#    return render_template('index.html')


@app.route('/', methods=['GET', 'POST'])
def monitor_price():
    if request.method == 'POST':
        price_low = float(request.form['price_low'])
        price_high = float(request.form['price_high'])

        response = requests.get(url).json()
        price = float(response['data']['amount'])

        if price > price_high:
            return send_message('Bitcoin price is above your threshold!')

        elif price < price_low:
            return send_message('Bitcoin price is below your threshold!')

    return render_template('index.html')


if __name__ == '__main__':
    app.run()


