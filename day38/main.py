# Exercise Tracking

import datetime as dt

import requests

import config

NUTRI_API_URL = "https://trackapi.nutritionix.com/v2"
SHEETY_API_URL = "https://api.sheety.co"
# these might or might not be the stats for Batman, from https://dc.fandom.com/wiki/Batman_(Bruce_Wayne)
GENDER = "male"
WEIGHT_KG = 95
HEIGHT_CM = 188
AGE = 35


def get_calories(text):
    """Takes a description of exercises as a STR and returns a LIST of data."""
    exercise_url = f"{NUTRI_API_URL}/natural/exercise"
    body = {
        "query": text,
        "gender": GENDER,
        "weight_kg": WEIGHT_KG,
        "height_cm": HEIGHT_CM,
        "age": AGE
    }
    # x-remote-user-id is just to specify
    headers = {
        "x-app-id": config.NUTRI_APP_ID,
        "x-app-key": config.NUTRI_API_KEY,
        "x-remote-user-id": "0"
    }
    response = requests.post(url=exercise_url, json=body, headers=headers)
    # just raise an error if there's a issue
    response.raise_for_status()
    # return just the list of exercises
    return response.json()["exercises"]


def add_entry(entry):
    """Takes a DICT and adds the contents to the defined spreadsheet."""
    sheet_url = SHEETY_API_URL + config.SHEET_URL
    # these are the names of the columns in the sheet
    # using today's date and the current time
    body = {
        "workout": {
            "date": dt.datetime.now().strftime("%Y-%m-%d"),
            "time": dt.datetime.now().strftime("%H:%M"),
            "exercise": entry["user_input"].capitalize(),
            "duration": f"{entry['duration_min']} min",
            "calories": f"{entry['nf_calories']} kcal"
        }
    }
    headers = {
        "Authorization": f"Bearer {config.SHEETY_TOKEN}"
    }
    response = requests.post(url=sheet_url, json=body, headers=headers)
    # also just raise an error
    response.raise_for_status()
    # to have some feedback
    print(response.content)


# just to have some basic interaction
print("What exercises have you done today?")
while True:
    activity = input("> ")
    if activity == "":
        print("Please enter an exercise.")
    else:
        break
# get a list with data for each activity
exercise_list = get_calories(activity)
# create an entry for each recognized exercise
for exercise in exercise_list:
    add_entry(exercise)
