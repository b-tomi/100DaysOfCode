# Flight Deal Finder

import datetime as dt

import data_manager as dm
import flight_search as fs
import notification_manager as nm

ORIGIN_CODE = "LON"

# initialization
data_manager = dm.DataManager()
flight_search = fs.FlightSearch()
notification_manager = nm.NotificationManager()

# load the spreadsheet
sheet = data_manager.get_sheet()

# add missing codes
for city in sheet:
    if city["iataCode"] == "":
        query_result = flight_search.find_city_code(city["city"])
        city["iataCode"] = query_result[0]["code"]
        # update the row in the spreadsheet
        data_manager.update_entry(city)

for city in sheet:
    # using the default time zone
    today = dt.datetime.now()
    tomorrow = today + dt.timedelta(days=1)
    in_six_months = today + dt.timedelta(days=(6 * 30))
    # get a flight object with the details
    flight = flight_search.find_flights(origin=ORIGIN_CODE, destination=city["iataCode"],
                                        date_from=tomorrow.strftime("%d/%m/%Y"),
                                        date_to=in_six_months.strftime("%d/%m/%Y"))

    # send an sms if price is lower than defined in the spreadsheet
    if flight.price <= city["lowestPrice"]:
        # to have some feedback
        print("Sending a notification.")
        notification_manager.send_sms(flight)
