# Amazon Price Tracker

import smtplib

import requests
from bs4 import BeautifulSoup

import config

# using the product suggested by the course
PAGE_URL = "https://www.amazon.com/Instant-Pot-Duo-Evo-Plus/dp/B07W55DDFB/"
# get a notification whenever the price falls below the following
TARGET_PRICE = 100
CURRENCY = "$"
# default Mailtrap server settings
SMTP_SERVER = "smtp.mailtrap.io"
SMTP_PORT = "2525"
# not really necessary, but might as well format the email properly
SENDER_NAME = "Amazon Price Tracker"
SENDER_ADDRESS = "pricetracker@mydomain.zyx"
SUBJECT_TEXT = "Amazon Price Tracker Price Alert"
# "Amazon Price Tracker Price Alert Recipient" sounded a little impersonal...
# so using one of the names from Day 40 instead
RECEIVER_NAME = "Anita Bath"
RECEIVER_ADDRESS = "myemail@mydomain.zyx"


def get_price():
    """Retrieves the price from the defined page and returns it as a FLOAT."""
    # pretend to be a proper web browser, essentially
    headers = {
        "Accept-Language": "en-US,en;q=0.9,ja-JP;q=0.8,ja;q=0.7",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/87.0.4280.141 Safari/537.36 "
    }
    response = requests.get(url=PAGE_URL, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    # using an id that's unique to the page
    result = soup.select_one("#price_inside_buybox")
    raw_price = result.get_text()
    # just return the value
    try:
        price_num = float(raw_price.replace("$", ""))
    except ValueError:
        return None
    else:
        return price_num


def send_email(price):
    """Takes a price as a FLOAT and sends an email alert using the defined parameters."""
    # format the email for the SMTP server
    sender = f"{SENDER_NAME} <{SENDER_ADDRESS}>"
    receiver = f"{RECEIVER_NAME} <{RECEIVER_ADDRESS}>"
    message = f"Subject: {SUBJECT_TEXT}\nTo: {receiver}\nFrom: {sender}\n\n" \
              f"The following product is now {CURRENCY}{price} (below the defined {CURRENCY}{TARGET_PRICE}).\n\n" \
              f"{PAGE_URL}"
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(config.SMTP_LOGIN, config.SMTP_PASS)
            server.sendmail(sender, receiver, message)
    except smtplib.SMTPServerDisconnected as ex:
        print(ex)
        print("Make sure the SMTP_LOGIN and SMTP_PASS credentials have been set correctly in config.py.")
    else:
        # just to have some feedback
        print(f"A price alert was sent to {RECEIVER_ADDRESS}.")


# get the current price
current_price = get_price()

if current_price is None:
    print("Could not retrieve the current price.")
# convert to float, just to be safe
elif current_price <= float(TARGET_PRICE):
    send_email(current_price)
