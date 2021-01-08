# SMS Rain Alert

import requests
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

# a random location in Europe from Day 33
MY_LAT = 37.7550636464
MY_LONG = 14.995246019
# time span to check (in hours, max. 48)
TIME_SPAM = 12
OWM_API_URL = "https://api.openweathermap.org/data/2.5/onecall"

# keeping these here for simplicity, generally they would be stored more securely
# register for a free account at https://openweathermap.org/ to get an API key
OWM_API_KEY = "myapikey"
# register for a free trial account at https://www.twilio.com/ to get an ACCOUNT SID & AUTH TOKEN
TWILIO_SID = "mysid"
TWILIO_TOKEN = "mytoken"
# Twilio phone number to send the SMS from
TWILIO_NUMBER = "notmynumber"
# real phone number to send the SMS to
TARGET_NUMBER = "mynumber"

params = {
    "lat": MY_LAT,
    "lon": MY_LONG,
    "exclude": "current,minutely,daily",
    "appid": OWM_API_KEY
}
response = requests.get(OWM_API_URL, params=params)
# a simple error message, at least
if response.status_code != 200:
    print(response.text)
    print("Make sure the OWM_API_KEY is set properly.")
    response.raise_for_status()
# only need the "hourly" data, not the generic location, etc. part
weather_data = response.json()["hourly"]

rainy_forecast = True
# check the hourly forecast
for i in range(TIME_SPAM):
    # used just for testing, this prints out a simple description of the forecast
    # print(f"In {i} hour(s): {weather_data[i]['weather'][0]['main']}")
    # condition id codes listed at https://openweathermap.org/weather-conditions
    # 2xx: Thunderstorm, 3xx: Drizzle, 5xx: Rain, 6xx: Snow, etc.
    if int(weather_data[i]["weather"][0]["id"]) < 700:
        rainy_forecast = True
        # no need to check the rest
        break

if rainy_forecast:
    # Twilio python docs: https://www.twilio.com/docs/sms/quickstart/python
    try:
        client = Client(TWILIO_SID, TWILIO_TOKEN)
        message = client.messages.create(body="It's going to rain today. Remember to bring an umbrella.",
                                         from_=TWILIO_NUMBER, to=TARGET_NUMBER)
    except TwilioRestException as ex:
        # a generic error message
        print(ex)
        print("Make sure the TWILIO_SID, TWILIO_TOKEN, TWILIO_NUMBER and TARGET_NUMBER are set properly.")
    else:
        # print the status for verification
        print(message.status)
