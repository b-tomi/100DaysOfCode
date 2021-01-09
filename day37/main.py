# Habit Tracking

import datetime as dt

import requests

import config

PIXELA_API_URL = "https://pixe.la/v1/users"
# set this to False once the user and graph have been created and config.py has been updated
new_user = True


def create_user():
    params = {
        "token": config.PIXELA_TOKEN,
        "username": config.PIXELA_USERNAME,
        "agreeTermsOfService": "yes",
        "notMinor": "yes",
        "thanksCode": "ThisIsThanksCode"
    }
    # sending data using .post
    response = requests.post(url=PIXELA_API_URL, json=params)
    # print for reference
    print(response.text)


def create_graph():
    graph_url = f"{PIXELA_API_URL}/{config.PIXELA_USERNAME}/graphs"
    # hard-coding the graph id, etc. since only a single graph will be used
    params = {
        "token": config.PIXELA_TOKEN,
        "username": config.PIXELA_USERNAME,
        "id": "graph1",
        "name": "Cycling Graph",
        "unit": "Km",
        "type": "float",
        "color": "ajisai"
    }
    # the password needs to be sent separately
    headers = {
        "X-USER-TOKEN": config.PIXELA_TOKEN
    }
    response = requests.post(url=graph_url, json=params, headers=headers)
    # print for reference
    print(response.text)


def add_value(quantity):
    # again, hard-coding the graph id since only a single graph is used
    graph_url = f"{PIXELA_API_URL}/{config.PIXELA_USERNAME}/graphs/graph1"
    # get and format the date the same way as in Day 36
    params = {
        "date": dt.datetime.today().strftime("%Y%m%d"),
        "quantity": str(quantity)
    }
    headers = {
        "X-USER-TOKEN": config.PIXELA_TOKEN
    }
    response = requests.post(url=graph_url, json=params, headers=headers)
    # print for reference
    print(response.text)


def update_value(date, quantity):
    value_url = f"{PIXELA_API_URL}/{config.PIXELA_USERNAME}/graphs/graph1/{date}"
    # the quantity key needs a STR value
    params = {
        "quantity": str(quantity)
    }
    headers = {
        "X-USER-TOKEN": config.PIXELA_TOKEN
    }
    response = requests.put(url=value_url, json=params, headers=headers)
    # print for reference
    print(response.text)


def delete_value(date):
    value_url = f"{PIXELA_API_URL}/{config.PIXELA_USERNAME}/graphs/graph1/{date}"
    headers = {
        "X-USER-TOKEN": config.PIXELA_TOKEN
    }
    response = requests.delete(url=value_url, headers=headers)
    # print for reference
    print(response.text)


# only need to run these once
if new_user:
    create_user()
    create_graph()
else:
    # just to have some basic interaction
    print("How many Kms did you cycle today?")
    while True:
        raw_input = input("> ")
        try:
            float_input = float(raw_input)
        except ValueError:
            print("Please enter a number value.")
        else:
            break

    # add the new value for the current day
    add_value(float_input)

    # update a value, needs the date of the pixel as a STR, eg. "20210109"
    # update_value("20210109", 12.3)

    # delete a value, also needs the date of the pixel as a STR
    # delete_value("20210109")
