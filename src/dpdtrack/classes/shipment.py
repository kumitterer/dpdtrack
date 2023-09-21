from typing import List, Optional, Tuple
from datetime import datetime

class Event:
    """ A class representing an individual event. """

    timestamp: datetime
    description: str
    location: str
    raw: str

class Shipment:
    """ A class representing a shipment. """

    tracking_number: str
    courier: str
    events: Optional[List[Event]] = None
    foreign: Optional[Tuple[str, str]] = None
    raw: str