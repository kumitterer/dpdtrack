from hashlib import md5
from configparser import ConfigParser
from urllib.parse import urlencode

import json

from .http import HTTPRequest


class GLSAPI:
    COUNTRY_CODE = "GB"
    LANGUAGE_CODE = "en"
    BASE_URL = "https://gls-group.eu/app/service/open/rest/"

    def __init__(self, country_code: str = COUNTRY_CODE, language_code: str = LANGUAGE_CODE, base_url: str = BASE_URL):
        self.country_code = country_code.upper()
        self.language_code = language_code.lower()
        self.base_url = base_url

    def get_request(self, endpoint: str, parameters: dict = {}) -> HTTPRequest:
        url = f"{self.base_url}/{self.country_code}/{self.language_code}/{endpoint}{f'?{urlencode(parameters)}' if parameters else ''}"
        request = HTTPRequest(url)
        return request

    def tracking(self, tracking_number: str):
        endpoint = "rstt001"
        parameters = {
            "match": tracking_number,
        }

        request = self.get_request(endpoint, parameters)
        response = request.execute()
        return response