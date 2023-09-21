from hashlib import md5
from configparser import ConfigParser
from urllib.parse import urlencode
from datetime import datetime

import json

import bs4

from .http import HTTPRequest
from .shipment import Shipment, Event

class DPDAT:
    """ DPD Austria API 
    
    This API is used to track packages in Austria. It also seems to work for
    packages in Germany, but this is not extensively tested.
    """

    SEARCH = "https://www.mydpd.at/jws.php/parcel/search"
    VERIFY = "https://www.mydpd.at/jws.php/parcel/verify"

    def tracking(self, tracking_number: str, **kwargs):
        """ Search for a tracking number """

        postal_code = kwargs.get("postal_code", None)
        wrap = kwargs.get("wrap", False)

        if postal_code is None:
            endpoint = self.SEARCH
            payload = tracking_number
        else:
            endpoint = self.VERIFY
            payload = [tracking_number, postal_code]

        request = HTTPRequest(endpoint)
        request.add_json_payload(payload)

        response = request.execute()

        if not wrap:
            return response

        shipment = Shipment()
        shipment.tracking_number = response["data"][0]["pno"]
        shipment.courier = self.__class__.__name__

        shipment.events = []

        for event in response["data"][0]["lifecycle"]["entries"]:
            event_obj = Event()

            if "depotData" in event and event["depotData"] is not None:
                event_obj.location = ", ".join(event['depotData'])
            else:
                event_obj.location = None

            event_obj.timestamp = datetime.strptime(event["datetime"], "%Y%m%d%H%M%S")
            event_obj.description = event['state']['text']
            event_obj.raw = json.dumps(event)

            shipment.events.append(event_obj)

        shipment.raw = json.dumps(response)

        return shipment

class DPDRO:
    """ DPD Romania API """

    URL = "https://tracking.dpd.ro/?shipmentNumber=%s&language=%s"

    def tracking(self, tracking_number: str, **kwargs):
        """ Search for a tracking number """

        language = kwargs.get("language", "en")
        wrap = kwargs.get("wrap", False)

        request = HTTPRequest(self.URL % (tracking_number, language))
        response = request.execute(False).decode()

        if not wrap:
            return response

        response = bs4.BeautifulSoup(response, features="html.parser")

        shipment = Shipment()

        header_table = response.find("span", {"class", "spanTableHeader"})
        shipment.tracking_number = header_table.text.split()[0]
        shipment.courier = self.__class__.__name__

        if remote_data := header_table.find("a"):
            remote_courier = remote_data.get("href")
            if "dpd.de" in remote_courier:
                remote_courier = "DPDDE"
            elif "mydpd.at" in remote_courier:
                remote_courier = "DPDAT"

            shipment.remote = [(remote_data.text, remote_courier)]

        shipment.events = []

        data_table = response.find("table", {"class": "standard-table"})

        for row in data_table.find_all("tr")[1:]:
            event_obj = Event()
            
            date, time, event_obj.description, event_obj.location = row.find_all("td")

            event_obj.timestamp = datetime.strptime(f"{date.text} {time.text}", "%d.%m.%Y %H:%M:%S")
            event_obj.raw = row.prettify()

            shipment.events.append(event_obj)

        shipment.raw = response.prettify()

        return shipment