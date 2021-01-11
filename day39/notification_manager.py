from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

import config


class NotificationManager:

    def __init__(self):
        # not handling any exceptions for now, this will return a "TwilioException" if credentials are not set
        self.client = Client(config.TWILIO_SID, config.TWILIO_TOKEN)

    def send_sms(self, flight):
        """Takes a flight object and sends the details as an SMS to the defined number."""
        message = f"Low Price alert! Only {flight.price} to fly from {flight.origin_city}-{flight.origin_airport} " \
                  f"to {flight.destination_city}-{flight.destination_airport}, " \
                  f"from {flight.leave_date} to {flight.return_date}."
        # re-using the code from Day 36, with minor changes
        try:
            message = self.client.messages.create(body=message, from_=config.TWILIO_NUMBER, to=config.TARGET_NUMBER)
        except TwilioRestException as ex:
            # a generic error message that will get displayed with each failed attempt
            print(ex)
            print("Make sure the TWILIO_SID, TWILIO_TOKEN, TWILIO_NUMBER and TARGET_NUMBER are set properly in "
                  "config.py.")
        else:
            print(message.status)
