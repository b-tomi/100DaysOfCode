# ISS Overhead Notifier

import requests
import datetime as dt
import time

# a random location in Europe
# NB: might or might not be in the middle of a volcano
MY_LAT = 37.7550636464
MY_LONG = 14.995246019
ISS_JSON = "http://api.open-notify.org/iss-now.json"
SUN_JSON = "https://api.sunrise-sunset.org/json"


def get_iss_location():
    """Gets the current location of the ISS, returns it as a TUPLE."""
    # get the current location of the ISS
    response = requests.get(url=ISS_JSON)
    response.raise_for_status()
    iss_location = response.json()
    # return as a tuple
    return float(iss_location["iss_position"]["latitude"]), float(iss_location["iss_position"]["longitude"])


def is_iss_nearby(pos):
    """Takes a location as a TUPLE and returns TRUE if it's near the defined position."""
    # de-structure the tuple, for the sake of readability
    iss_lat, iss_long = pos
    # if the ISS is within +5 or -5 degrees of the defined position
    if abs(MY_LAT - iss_lat) < 5 and abs(MY_LONG - iss_long) < 5:
        return True
    # it's not actually necessary to include this line
    return False


def is_nighttime():
    """Returns TRUE if it's nighttime at the defined location."""
    # get the sunset and sunrise times for the current location
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }
    response = requests.get(SUN_JSON, params=parameters)
    response.raise_for_status()
    daytime = response.json()
    sunset = int(daytime["results"]["sunset"].split("T")[1].split(":")[0])
    sunrise = int(daytime["results"]["sunrise"].split("T")[1].split(":")[0])

    # get the current hour as UTC, to match the above
    now = dt.datetime.utcnow().hour

    # true if it's after sunset or before next sunrise
    if now >= sunset or now <= sunrise:
        return True
    # just to be consistent
    return False


# run indefinitely while checking every 60 seconds
while True:
    if is_iss_nearby(get_iss_location()) and is_nighttime():
        # rather than sending an email, just print a line
        print("Look up!\nThe ISS is above you in the sky.")
    time.sleep(60)
