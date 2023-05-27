import time
import requests
import os
from datetime import datetime

def make_http_call():
    url = 'https://api.spot-hinta.fi/JustNow'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # Process the response data as needed
        send_to_discord(data)
    else:
        print('HTTP request failed with status code {}'.format(response.status_code))

def send_to_discord(data):
    price_with_tax = data.get('PriceWithTax')
    price_no_tax = data.get('PriceNoTax')
    timestamp = data.get('DateTime')
    if price_with_tax is not None:
        # Discord webhook URL
        url = os.environ.get('DISCORD_WEBHOOK_URL')
        headers = {'Content-Type': 'application/json'}

        # Multiply prices by 100 to convert to cents
        price_with_tax_cents = price_with_tax * 100
        price_no_tax_cents = price_no_tax * 100

        # Format the date and time using datetime
        datetime_obj = datetime.strptime(timestamp[:-6], "%Y-%m-%dT%H:%M:%S")
        datetime_formatted = datetime_obj.strftime("%Y-%m-%d %H:%M")

        # Role mention
        role_mention = '<@&1111346943273205770>'

        payload = {
            'content': '{}'.format(role_mention),
            'embeds': [
                {
                    'title': 'Price Information',
                    'description': 'Price (with tax):\n{:.2f} c/kWh\nPrice (without tax):\n{:.2f} c/kWh'.format(price_with_tax_cents, price_no_tax_cents),
                    'color': 16776960,  # Yellow color code
                    'thumbnail': {
                        'url': 'https://icons-for-free.com/iconfiles/png/512/electricity+icon-1320087270769193842.png',
                        'height': 100,
                        'width': 100
                    },
                    'footer': {
                        'text': '🕘 ' + datetime_formatted
                    }
                }
            ]
        }
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code != 204:
            print('Failed to send data to Discord with status code {}'.format(response.status_code))

def wait_for_next_hour():
    # Get the current time
    current_time = time.localtime()
    # Calculate the number of seconds remaining until the next full hour
    seconds_remaining = 3600 - (current_time.tm_min * 60 + current_time.tm_sec)
    # Wait until the next full hour
    time.sleep(seconds_remaining)

# Run the script indefinitely
while True:
    # Wait until the next full hour
    wait_for_next_hour()
    # Make the HTTP call
    make_http_call()