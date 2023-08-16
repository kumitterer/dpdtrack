# KeyDelivery API Python Client

This is a Python client for the KeyDelivery API. It is a wrapper around the [KeyDelivery](https://kd100.com/) API, which allows you to track your shipments.

It is not fully featured yet, but it is a good starting point.

## Installation

```bash
pip install git+https://kumig.it/kumitterer/pykeydelivery
```

## Usage

```python
from keydelivery import KeyDelivery

api = KeyDelivery("YOUR_API_KEY", "YOUR_API_SECRET")

# Find carrier by shipment number

carrier_options = api.detect_carrier("YOUR_SHIPMENT_NUMBER")

# Realtime tracking

tracking = api.realtime("CARRIER_CODE", "YOUR_SHIPMENT_NUMBER")
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.