import requests
from twilio.rest import Client
import sys
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import os
from dotenv import load_dotenv

# Load environment variables from .env
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

# Twilio account SID and auth token
account_sid = os.getenv('ACCOUNT_SID')
auth_token = os.getenv('AUTH_TOKEN')

# Twilio phone number and your own phone number
twilio_number = os.getenv('TWILIO_NUMBER')
your_number = os.getenv('YOUR_NUMBER')

# Ask for which prices to be alerted at
#price_high = float(input("What price of $BTC do you want to be alerted at if it goes over? "))
#price_low = float(input("What price of $BTC do you want to be alerted at if it goes under? "))
price_low = float(sys.argv[1])
price_high = float(sys.argv[2])
#print('-'*100)
print(f'Range: {price_low} - {price_high}')

# Flag variable to keep track of whether the notification has been sent
notification_sent = False

# Function to send a text message using Twilio
def send_message(message):
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=message,
        from_=twilio_number,
        to=your_number
    )
    print('Message sent!')
    sys.exit(0)

# Print price at start time
#requests.get(url).json()
#float(response['data']['amount'])
#print('Current Bitcoin Price: ${:,.2f}'.format(price))

# If the current Bitcoin price is below or above the threshold and a notification hasn't been sent yet, SEND IT
while not notification_sent:
    response = requests.get(url).json()
    price = float(response['data']['amount'])
#    print('Current Bitcoin price: ${:,.2f}'.format(price))

    # Send a text message if the price goes above or below threshold
    if price > price_high:
        send_message('Bitcoin price is above your threshold!')
        notification_sent = True

    elif price < price_low:
        send_message('Bitcoin price is below your threshold!')
        notification_sent = True

    # Wait for 1 minute before checking the price again
    time.sleep(10)

