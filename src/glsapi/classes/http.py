from urllib.request import Request, urlopen

import json


class HTTPRequest(Request):
    USER_AGENT = "Mozilla/5.0 (compatible; GLSAPI/dev; +https://kumig.it/kumitterer/glsapi)"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_header("User-Agent", self.USER_AGENT)

    def execute(self, load_json: bool = True, *args, **kwargs):
        response = urlopen(self, *args, **kwargs).read()
        if load_json:
            response = json.loads(response)
        return response
