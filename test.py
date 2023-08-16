from unittest import TestCase, main
from configparser import ConfigParser

import json

from pykeydelivery import *

class TestHTTPRequest(TestCase):
    def test_http_request(self):
        http = HTTPRequest("https://httpbin.org/get")
        response = http.execute()
        self.assertEqual(response["headers"]["User-Agent"], http.USER_AGENT)

    def test_http_request_with_json_payload(self):
        http = HTTPRequest("https://httpbin.org/post")
        http.add_json_payload({"foo": "bar"})
        response = http.execute()
        self.assertEqual(response["headers"]["User-Agent"], http.USER_AGENT)
        self.assertEqual(response["headers"]["Content-Type"], "application/json")
        self.assertEqual(response["json"]["foo"], "bar")

class TestKeyDelivery(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = ConfigParser()
        self.config.read("config.ini")
        self.keydelivery = KeyDelivery.from_config(self.config)

    def test_detect_carrier(self):
        response = self.keydelivery.detect_carrier("483432314669")
        self.assertEqual(response["code"], 200)

    def test_realtime(self):
        response = self.keydelivery.realtime("gls", "483432314669")
        self.assertEqual(response["code"], 200)
        
if __name__ == "__main__":
    main()