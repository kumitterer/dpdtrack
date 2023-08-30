# myDPD Python Client

This is a Python client for the myDPD Austria (https://mydpd.at) tracker. It allows you to track your shipments.

It currently *only* supports DPD Austria. If you want to add support for other countries, feel free to open a pull request. Tracking for DPD shipments in other countries *may* work, but it is not guaranteed.

## Installation

```bash
pip install dpdtrack
```

## Usage

```python
from dpdtrack import DPD

api = DPD()

# Realtime tracking

tracking = api.tracking("YOUR_SHIPMENT_NUMBER")

# Optionally pass the recipient's postal code to get more accurate results

tracking = api.tracking("YOUR_SHIPMENT_NUMBER", "RECIPIENT_POSTAL_CODE")
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.