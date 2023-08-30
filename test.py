from unittest import TestCase, main
from configparser import ConfigParser

import json

from dpdtrack import *

class TestHTTPRequest(TestCase):
    def test_http_request(self):
        http = HTTPRequest("https://httpbin.org/get")
        response = http.execute()
        self.assertEqual(response["headers"]["User-Agent"], http.USER_AGENT)

class TestDPD(TestCase):
    def setUp(self):
        self.api = DPD()

    def test_tracking(self):
        tracking_number = "01155036780055"
        response = self.api.tracking(tracking_number)
        self.assertEqual(response["state"], "success")
        self.assertEqual(response["data"][0]["pno"], tracking_number)

    def test_tracking_with_postal_code(self):
        tracking_number = "01155036780055"
        postal_code = "8010"
        response = self.api.tracking(tracking_number, postal_code)
        self.assertEqual(response["state"], "success")
        self.assertEqual(response["data"][0]["pno"], tracking_number)