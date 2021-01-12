import smtplib

from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

import config

# the default Mailtrap server settings
SMTP_SERVER = "smtp.mailtrap.io"
SMTP_PORT = "2525"


class NotificationManager:

    def __init__(self):
        # not handling any exceptions for now, this will return a "TwilioException" if credentials are not set
        self.server = SMTP_SERVER
        self.port = SMTP_PORT
        self.client = Client(config.TWILIO_SID, config.TWILIO_TOKEN)
        self.sender = f"{config.SENDER_NAME} <{config.SENDER_ADDRESS}>"

    def send_sms(self, flight):
        """Takes a flight object and sends the details as an SMS to the defined number."""
        message = f"Low Price alert! Only {flight.price} to fly from {flight.origin_city}-{flight.origin_airport} " \
                  f"to {flight.destination_city}-{flight.destination_airport}, " \
                  f"from {flight.leave_date} to {flight.return_date}."
        # if it's not a direct flight
        if flight.stopovers > 0:
            # only expecting max. 1 stopover
            message += f"\nThe flight has {flight.stopovers} stop over, via {flight.via_city}."
        # re-using the code from Day 36, with minor changes
        print(message)
        try:
            message = self.client.messages.create(body=message, from_=config.TWILIO_NUMBER, to=config.TARGET_NUMBER)
        except TwilioRestException as ex:
            # a generic error message that will get displayed with each failed attempt
            print(ex)
            print("Make sure the TWILIO_SID, TWILIO_TOKEN, TWILIO_NUMBER and TARGET_NUMBER are set properly in "
                  "config.py.")
        else:
            print(message.status)

    def notify_users(self, flight, users):
        for user in users:
            receiver = f"{user['firstName']} {user['lastName']} <{user['email']}>"
            message = f"Subject: Low Price Alert from {config.SENDER_NAME}\nTo: {receiver}\nFrom: {self.sender}\n\n" \
                      f"Low Price alert! Only {flight.price} to fly from {flight.origin_city}-{flight.origin_airport}" \
                      f" to {flight.destination_city}-{flight.destination_airport}, " \
                      f"from {flight.leave_date} to {flight.return_date}.\n\n" \
                      f"https://www.google.co.uk/flights?hl=en#flt=" \
                      f"{flight.origin_airport}.{flight.destination_airport}.{flight.leave_date}*" \
                      f"{flight.destination_airport}.{flight.origin_airport}.{flight.return_date}"
            self.send_email(self.sender, receiver, message)

    def send_email(self, sender, receiver, message):
        try:
            with smtplib.SMTP(self.server, self.port) as server:
                server.starttls()
                server.login(config.SMTP_LOGIN, config.SMTP_PASS)
                server.sendmail(sender, receiver, message)
        except smtplib.SMTPServerDisconnected:
            print("ERROR: Could not connect to the SMTP server. "
                  "Make sure the SMTP_LOGIN and SMTP_PASS credentials have been set correctly.")
        except smtplib.SMTPDataError:
            # in case too many emails are being sent in a short time
            # handling this properly is really not in the scope of this project
            print(f"ERROR: Too many emails per second. The message to {receiver} was not sent.")
        else:
            # just to have some feedback
            print(f"The message to {receiver} was sent.")
