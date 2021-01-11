import requests

import config

SHEETY_API_URL = "https://api.sheety.co"


class DataManager:

    def __init__(self):
        self.sheet_url = SHEETY_API_URL + config.SHEET_URL
        # this is the same for all operations
        self.headers = {
            "Authorization": f"Bearer {config.SHEETY_TOKEN}"
        }

    def get_sheet(self):
        """Retrieves the spreadsheet and returns the rows as a LIST."""
        response = requests.get(url=self.sheet_url, headers=self.headers)
        # just raise an error, not handling exceptions for now
        response.raise_for_status()
        # to have some feedback
        print("Spreadsheet successfully loaded.")
        return response.json()["prices"]

    def update_entry(self, entry):
        """Takes a row number as STR and updates the corresponding row in the spreadsheet."""
        edit_url = f"{self.sheet_url}/{entry['id']}"
        body = {
            "price": {
                "iataCode": entry["iataCode"]
            }
        }
        response = requests.put(url=edit_url, json=body, headers=self.headers)
        # also just raise an error
        response.raise_for_status()
        # also to have some feedback
        print(f"Row {entry['id']} has been updated with code {entry['iataCode']}.")
