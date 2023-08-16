from hashlib import md5
from configparser import ConfigParser

import json

from .http import HTTPRequest


class KeyDelivery:
    BASE_URL = "https://www.kd100.com/api/v1/"

    def __init__(self, key: str, secret: str, base_url: str = BASE_URL):
        self.key = key
        self.secret = secret
        self.base_url = base_url

    @classmethod
    def from_config(cls, config: ConfigParser | str, section: str = "KeyDelivery") -> "KeyDelivery":
        if isinstance(config, str):
            temp_config = ConfigParser()
            temp_config.read(config)
            config = temp_config

        key = config.get(section, "key")
        secret = config.get(section, "secret")
        base_url = config.get(section, "base_url", fallback=cls.BASE_URL)

        return cls(key, secret, base_url)

    def get_signature(self, message: dict) -> str:
        content = json.dumps(message)
        data = (content + self.key + self.secret).encode("utf-8")
        return md5(data).hexdigest().upper()

    def get_request(self, endpoint: str, message: dict) -> HTTPRequest:
        url = self.base_url + endpoint
        signature = self.get_signature(message)

        request = HTTPRequest(url)
        request.add_json_payload(message)
        request.add_header("API-Key", self.key)
        request.add_header("signature", signature)

        return request

    def realtime(self, carrier: str, tracking_number: str) -> bytes:
        message = {
            "carrier_id": carrier,
            "tracking_number": tracking_number,
        }

        request = self.get_request("tracking/realtime", message)
        return request.execute()

    def detect_carrier(self, tracking_number: str) -> bytes:
        message = {
            "tracking_number": tracking_number,
        }

        request = self.get_request("carriers/detect", message)
        return request.execute()
