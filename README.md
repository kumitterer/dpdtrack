# GLS REST API Python Client

This is a Python client for the GLS (https://gls-group.eu) REST API. It allows you to track your shipments.

It currently only supports package tracking, not any other API endpoints.

## Installation

```bash
pip install glsapi
```

## Usage

```python
from glsapi import GLSAPI

api = GLSAPI()

carrier_options = api.detect_carrier("YOUR_SHIPMENT_NUMBER")

# Realtime tracking

tracking = api.tracking("YOUR_SHIPMENT_NUMBER")
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.