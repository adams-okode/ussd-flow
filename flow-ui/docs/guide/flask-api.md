# UssdFlow with Flask

## Installation

Install Flask and UssdFlow using pip:

```bash
pip install flask ussdflow
```

## Flask Application

Create an `app.py` file for your Flask application:

```python
from flask import Flask, request, jsonify
from ussdflow import CacheManager, IngressData, USSDService

app = Flask(__name__)

# Initialize the cache manager
cache_manager = CacheManager(cache_type="redis", host="localhost", port=6379)

# Initialize the USSD service
ussd_service = USSDService(
    menu_file_path="path/to/your/menu.json",
    cache_manager=cache_manager
)

@app.route("/ussd/ingress", methods=["POST"])
def ingress():
    data = request.json
    ingress_data = IngressData(
        session_id=data["session_id"],
        service_code=data["service_code"],
        phone_number=data["phone_number"],
        text=data["text"],
        network_code=data["network_code"]
    )
    response = ussd_service.ingress(ingress_data)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
```

## Running the Flask Application

Run your Flask application:

```bash
python app.py
```
