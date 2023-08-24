from unittest import TestCase, main
from configparser import ConfigParser

import json

from glsapi import *

class TestHTTPRequest(TestCase):
    def test_http_request(self):
        http = HTTPRequest("https://httpbin.org/get")
        response = http.execute()
        self.assertEqual(response["headers"]["User-Agent"], http.USER_AGENT)

class TestGLSAPI(TestCase):
    def setUp(self):
        self.api = GLSAPI()

    def test_gls_api(self):
        tracking_number = "483432314669"
        response = self.api.tracking(tracking_number)
        unitno = [x for x in response["tuStatus"][0]["references"] if x["type"] == "UNITNO"][0]["value"]
        self.assertTrue(tracking_number.startswith(unitno))