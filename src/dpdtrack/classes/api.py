from hashlib import md5
from configparser import ConfigParser
from urllib.parse import urlencode

import json

from .http import HTTPRequest

class DPD:
    SEARCH = "https://www.mydpd.at/jws.php/parcel/search"
    VERIFY = "https://www.mydpd.at/jws.php/parcel/verify"

    def tracking(self, tracking_number: str, postal_code: str = None):
        if postal_code is None:
            endpoint = self.SEARCH
            payload = tracking_number
        else:
            endpoint = self.VERIFY
            payload = [tracking_number, postal_code]

        request = HTTPRequest(endpoint)
        request.add_json_payload(payload)

        response = request.execute()
        return response


