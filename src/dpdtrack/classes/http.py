from urllib.request import Request, urlopen

import json


class HTTPRequest(Request):
    USER_AGENT = "Mozilla/5.0 (compatible; DPDTrack/dev; +https://kumig.it/kumitterer/dpdtrack)"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_header("User-Agent", self.USER_AGENT)

    def execute(self, load_json: bool = True, *args, **kwargs):
        response = urlopen(self, *args, **kwargs).read()
        if load_json:
            response = json.loads(response)
        return response

    def add_json_payload(self, payload: dict):
        self.add_header("Content-Type", "application/json")
        self.data = json.dumps(payload).encode("utf-8")