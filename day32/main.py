# Automated Birthday Wisher

import datetime as dt
import pandas as pd
import random

import mailer

BIRTHDAYS_CSV = "birthdays.csv"
# modified these a little, so there's a custom sender name instead of "Angela"
TEMPLATE_LIST = [
    "./letter_templates/letter_1.txt",
    "./letter_templates/letter_2.txt",
    "./letter_templates/letter_3.txt",
]
SENDER_NAME = "Automated Birthday Wisher"
SENDER_ADDRESS = "myemail@mydomain.zyx"
# use the same subject line with each template
SUBJECT_TEXT = "Happy Birthday [RECEIVER_NAME]!"


def load_birthdays():
    """Loads the CSV file and returns the contents as a LIST."""
    df = pd.read_csv(BIRTHDAYS_CSV)
    # using list comprehension to create a list of dictionaries
    # "year" isn't actually needed, but including it for completeness' sake,
    # could be useful to calculate the person's age
    birthdays = [{"name": row[0], "email": row[1], "year": row[2], "month": row[3], "day": row[4]} for row in df.values]
    return birthdays


def generate_email(details):
    """Takes a DICT and sends an email to the provided address."""
    # create a mail object to store all parameters in
    mail = mailer.Email()
    # set the sender and receiver
    mail.set_sender(SENDER_NAME, SENDER_ADDRESS)
    mail.set_receiver(details["name"], details["email"])
    # set the subject, needs to be after the receiver has been set
    mail.set_subject(SUBJECT_TEXT)
    # choose a template
    mail.set_message(load_template())
    # send the email
    mail.send()


def load_template():
    """Loads a random template and returns it as a STR."""
    template = random.choice(TEMPLATE_LIST)
    with open(template, mode="r") as f:
        text = f.read()
    return text


# get today's date, including the "year" here as well
full_datetime = dt.datetime.now()
today = {
    "year": full_datetime.year,
    "month": full_datetime.month,
    "day": full_datetime.day
}
# load birthdays
birthdays_list = load_birthdays()
for person in birthdays_list:
    if person["month"] == today["month"] and person["day"] == today["day"]:
        # send a mail for each match
        generate_email(person)
