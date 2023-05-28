import time
import requests
import os
from datetime import datetime
import pytz

def make_http_call():
    url = 'https://api.spot-hinta.fi/Today'
    try:
        # Make an HTTP GET request to retrieve electricity price data
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception if the request was not successful (status code other than 200)
        data = response.json()  # Parse the response JSON
        current_hour_prices, next_hour_prices = get_current_and_next_hour_prices(data)
        if current_hour_prices and next_hour_prices:
            # Send the prices to Discord
            send_to_discord(current_hour_prices, next_hour_prices)
        else:
            print("Current or next hour's prices not available yet.")
    except requests.exceptions.RequestException as e:
        print('HTTP request failed:', e)

def get_current_and_next_hour_prices(data):
    # Specify the city's timezone
    city_timezone = pytz.timezone('Europe/Helsinki')

    # Get the current time in the specified timezone
    current_time = datetime.now(city_timezone)

    # Extract the current hour from the current time
    current_hour = current_time.hour

    current_hour_prices = None
    next_hour_prices = None

    # Find the current and next hour's prices from the data
    for item in data:
        datetime_str = item['DateTime']
        datetime_obj = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S%z")
        hour = datetime_obj.hour

        if hour == current_hour:
            current_hour_prices = item
        elif hour == current_hour + 1:
            next_hour_prices = item
            break

    return current_hour_prices, next_hour_prices

def send_to_discord(current_hour_prices, next_hour_prices):
    current_price_with_tax = current_hour_prices.get('PriceWithTax')
    current_price_no_tax = current_hour_prices.get('PriceNoTax')
    current_timestamp = current_hour_prices.get('DateTime')

    next_price_with_tax = next_hour_prices.get('PriceWithTax')
    next_price_no_tax = next_hour_prices.get('PriceNoTax')
    next_timestamp = next_hour_prices.get('DateTime')

    if current_price_with_tax is not None and next_price_with_tax is not None:
        url = os.environ.get('DISCORD_WEBHOOK_URL')
        headers = {'Content-Type': 'application/json'}

        # Convert prices to cents
        current_price_with_tax_cents = current_price_with_tax * 100
        current_price_no_tax_cents = current_price_no_tax * 100

        next_price_with_tax_cents = next_price_with_tax * 100
        next_price_no_tax_cents = next_price_no_tax * 100

        current_datetime_obj = datetime.strptime(current_timestamp, "%Y-%m-%dT%H:%M:%S%z")
        current_datetime_formatted = current_datetime_obj.strftime("%Y-%m-%d %H:%M")

        next_datetime_obj = datetime.strptime(next_timestamp, "%Y-%m-%dT%H:%M:%S%z")
        next_datetime_formatted = next_datetime_obj.strftime("%Y-%m-%d %H:%M")

        role_mention = '<@&1111346943273205770>'

        payload = {
            'content': '{}'.format(role_mention),
            'embeds': [
                {
                    'title': 'Electricity Price Information',
                    'description': '**Current Prices**\nWith tax: \n{:.2f} c/kWh\nWithout tax: \n{:.2f} c/kWh\n\n**Estimated Next Hour Prices**\nWith tax: \n{:.2f} c/kWh\nWithout tax: \n{:.2f} c/kWh'.format(current_price_with_tax_cents, current_price_no_tax_cents, next_price_with_tax_cents, next_price_no_tax_cents),
                    'color': 16776960,  # Yellow color code
                    'thumbnail': {
                        'url': 'https://icons-for-free.com/iconfiles/png/512/electricity+icon-1320087270769193842.png',
                        'height': 100,
                        'width': 100
                    },
                    'footer': {
                        'text': '🕘 {}'.format(current_datetime_formatted)
                    }
                }
            ]
        }
        try:
            # Make an HTTP POST request to send the data to Discord
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()  # Raise an exception if the request was not successful (status code other than 204)
        except requests.exceptions.RequestException as e:
            print('Failed to send data to Discord:', e)

def wait_for_next_hour():
    current_time = time.localtime()
    seconds_remaining = 3600 - (current_time.tm_min * 60 + current_time.tm_sec)
    time.sleep(seconds_remaining)

while True:
    wait_for_next_hour()
    make_http_call()