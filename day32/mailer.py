import smtplib

# utilizing https://mailtrap.io/ , a service specifically designed for testing similar apps
# their free account works just fine
SMTP_SERVER = "smtp.mailtrap.io"
SMTP_PORT = "2525"
# these need to be changed to valid credentials
SMTP_LOGIN = "mylogin"
SMTP_PASS = "mypassword"


class Email:

    def __init__(self):
        self.sender_name = ""
        self.sender_address = ""
        self.sender = ""
        self.receiver_name = ""
        self.receiver_address = ""
        self.receiver = ""
        self.subject = ""
        self.message = ""

    def set_sender(self, name, address):
        """Takes STRs and sets them as the sender's name an address."""
        self.sender_name, self.sender_address = name, address
        self.sender = f"{self.sender_name} <{self.sender_address}>"

    def set_receiver(self, name, address):
        """Takes STRs and sets them as the receiver's name an address."""
        self.receiver_name, self.receiver_address = name, address
        self.receiver = f"{self.receiver_name} <{self.receiver_address}>"

    def set_subject(self, subject):
        """Takes a STR and sets it as a subject"""
        self.subject = subject.replace("[RECEIVER_NAME]", self.receiver_name)

    def set_message(self, text):
        """Takes a template as STR and customizes it."""
        # in two steps just because it did not fit in a single line
        personalized_text = text.replace("[RECEIVER_NAME]", self.receiver_name)
        personalized_text = personalized_text.replace("[SENDER_NAME]", self.sender_name)
        self.message = f"""Subject: {self.subject}\nTo: {self.receiver}\nFrom: {self.sender}\n\n{personalized_text}"""

    def send(self):
        """Sends an email using the defined parameters."""
        if self.verify():
            try:
                with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                    server.starttls()
                    server.login(SMTP_LOGIN, SMTP_PASS)
                    server.sendmail(self.sender, self.receiver, self.message)
            except smtplib.SMTPServerDisconnected:
                print("ERROR: Could not connect to the SMTP server. "
                      "Make sure the SMTP_LOGIN and SMTP_PASS credentials have been set correctly.")
            else:
                # just to have some feedback
                print(f"The message to {self.receiver_name} at {self.receiver_address} was sent.")
        else:
            print(f"The message to {self.receiver_name} at {self.receiver_address} was NOT sent.")

    def verify(self):
        """Verifies that all required items have been specified."""
        # this is just to make sure everything works
        all_good = True
        for item in [self.subject, self.sender_name, self.sender_address, self.receiver_name, self.receiver_address,
                     self.message]:
            if item == "":
                # something slightly less vague might be more helpful, but this is just for debugging anyway
                print("Some of the parameters have not been specified.")
                all_good = False
                break
        return all_good
