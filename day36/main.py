# SMS Stock News

import datetime as dt

import requests
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

# moved API keys, etc. to a separate file config.py
# still need to be set to proper values
import config

# picking a stock that's somewhat volatile at the moment
STOCK = "SHOP"
COMPANY_NAME = "SHOPIFY INC"
# minimum percentual change to get an alert
MIN_CHANGE = 5
AV_API_URL = "https://www.alphavantage.co/query"
NEWS_API_URL = "http://newsapi.org/v2/everything"


def check_price(name):
    """Takes a name of a stock as STR and return a DICT with daily data for the previous days."""
    # Alpha Vantage docs: https://www.alphavantage.co/documentation/
    # When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
    # "outputsize" and "datatype" actually use their default values, but including them for sake of completeness
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": name,
        "outputsize": "compact",
        "datatype": "json",
        "apikey": config.AV_API_KEY
    }
    response = requests.get(AV_API_URL, params=params)
    # a simple error message
    if response.status_code != 200:
        print(response.text)
        print("Make sure the AV_API_KEY is set properly in config.py.")
        response.raise_for_status()
    # return just the daily data
    return response.json()["Time Series (Daily)"]


def calculate_change(data):
    """Takes a DICT and calculates the percentual change between the most recent days, returns it as a FLOAT."""
    # get a list of dates by converting the dict to a string
    # yesterday should be the first element, then the day before yesterday, etc.
    dates = list(data)
    # now it's possible to access the data for a particular date
    yesterday_closing = float(data[dates[0]]["4. close"])
    day_before_closing = float(data[dates[1]]["4. close"])
    # return the percentual change
    return (yesterday_closing - day_before_closing) / day_before_closing * 100


def get_news(name):
    """Takes a company name as a STR and returns a LIST of top related articles."""
    # News API docs: https://newsapi.org/docs/get-started
    # get today's date in a specific format
    today = dt.datetime.today().strftime("%Y-%m-%d")
    params = {
        "q": f"{name}&",
        "from": f"{today}&",
        "sortBy": "popularity&",
        "apikey": config.NEWS_API_KEY
    }
    response = requests.get(NEWS_API_URL, params=params)
    if response.status_code != 200:
        print(response.text)
        print("Make sure the NEWS_API_KEY is set properly in config.py.")
        response.raise_for_status()
    # return articles only
    return response.json()["articles"]


def send_sms(sms_text):
    """Takes a message as STR and sends it as an SMS to the defined number."""
    # re-using the code from Day 35, with minor changes
    try:
        client = Client(config.TWILIO_SID, config.TWILIO_TOKEN)
        message = client.messages.create(body=sms_text, from_=config.TWILIO_NUMBER, to=config.TARGET_NUMBER)
    except TwilioRestException as ex:
        # a generic error message that will get displayed with each failed attempt
        print(ex)
        print("Make sure the TWILIO_SID, TWILIO_TOKEN, TWILIO_NUMBER and TARGET_NUMBER are set properly in config.py.")
    else:
        print(message.status)


# get the daily data for the set stock
daily_data = check_price(STOCK)

# calculate the percentual change for the last two days
change = calculate_change(daily_data)

# if the change is more than the set minimum, up or down
if abs(change) >= MIN_CHANGE:
    # compose the message
    message_head = f"{STOCK}: "
    # add a mark depending on the movement
    if change >= MIN_CHANGE:
        message_head += "🔺"
    else:
        message_head += "🔻"
    # include the percentage
    message_head += f"{abs(round(change, 1))}%\n"

    # get news data for the company name
    news_data = get_news(COMPANY_NAME)
    # send a message with the top three articles
    for i in range(3):
        # clear the content before each iteration
        message_content = ""
        # add the titles and descriptions
        message_content += f"Headline: {news_data[i]['title']}\n"
        message_content += f"Brief: {news_data[i]['description'].strip('Summary List Placement')}"
        # send the sms
        send_sms(message_head + message_content)
