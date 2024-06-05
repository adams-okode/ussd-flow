# UssdFlow

UssdFlow is a dynamic and robust Python library designed to simplify the creation, management, and serving of USSD menus. Integrating seamlessly with Africa's Talking USSD implementation and utilizing Redis for efficient caching, UssdFlow aims to provide developers with a powerful tool to build interactive and responsive USSD applications.

## Key Features

- Dynamic Menu Creation: Easily define and manage USSD menus with dynamic content and options.
- Seamless Integration: Integrates directly with Africa's Talking USSD gateway for reliable and scalable USSD services.
- Efficient Caching: Leverages Redis for high-performance caching, ensuring quick and efficient session management.
- User Session Management: Handles user sessions effectively, tracking user progress through the USSD menus.
- Flexible Configuration: Offers flexible configuration options to tailor the USSD experience to specific needs.
- Error Handling: Robust error handling ensures smooth user interactions even when issues arise.

Installation
To install UssdFlow, simply use pip:

```bash
pip install ussdflow
```

## Getting Started

Here’s a quick example to get you started with UssdFlow:

```python
from ussdflow import CacheManager, IngressData, USSDService

# Initialize the cache manager

cache_manager = CacheManager(cache_type="redis", host="localhost", port=6379)

# Initialize the USSD service

ussd_service = USSDService(
    menu_file_path="path/to/your/menu.json",
    cache_manager=cache_manager
)

# Sample USSD request

request = IngressData(
    session_id="1234",
    service_code="*123#",
    phone_number="254712345678",
    text=""
)

# Process the request

response = ussd_service.ingress(request)
print(response)
```

## UssdFlow with Flask

### Installation

Install Flask and UssdFlow using pip:

```bash
pip install flask ussdflow
```

### Flask Application

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

### Running the Flask Application

Run your Flask application:

```bash
python app.py
```

## UssdFlow with FastAPI

### Installation

Install FastAPI, Uvicorn, and UssdFlow using pip:

```bash
pip install fastapi uvicorn ussdflow
```

### FastAPI Application

Create a `main.py` file for your FastAPI application:

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from ussdflow import CacheManager, IngressData, USSDService

app = FastAPI()

# Initialize the cache manager
cache_manager = CacheManager(cache_type="redis", host="localhost", port=6379)

# Initialize the USSD service
ussd_service = USSDService(
    menu_file_path="path/to/your/menu.json",
    cache_manager=cache_manager
)

class USSDRequest(BaseModel):
    session_id: str
    service_code: str
    phone_number: str
    text: str
    network_code: str

@app.post("/ussd/ingress")
def ingress(request: USSDRequest):
    try:
        ingress_data = IngressData(
            session_id=request.session_id,
            service_code=request.service_code,
            phone_number=request.phone_number,
            text=request.text,
            network_code=request.network_code
        )
        response = ussd_service.ingress(ingress_data)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Running the FastAPI Application

Run your FastAPI application:

```bash
uvicorn main:app --reload
```

## UssdFlow with Django

### Installation

Install Django and UssdFlow using pip:

```bash
pip install django ussdflow
```

### Django Project and Application Setup

1. Create a new Django project and application:

```bash
django-admin startproject ussdproject
cd ussdproject
django-admin startapp ussdapp
```

2. Add `ussdapp` to your `INSTALLED_APPS` in `settings.py`:

```python
# ussdproject/settings.py

INSTALLED_APPS = [
    ...
    'ussdapp',
]
```

3. Create a view in `ussdapp/views.py`:

```python
# ussdapp/views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from ussdflow import CacheManager, IngressData, USSDService

# Initialize the cache manager
cache_manager = CacheManager(cache_type="redis", host="localhost", port=6379)

# Initialize the USSD service
ussd_service = USSDService(
    menu_file_path="path/to/your/menu.json",
    cache_manager=cache_manager
)

@csrf_exempt
def ingress(request):
    if request.method == "POST":
        data = json.loads(request.body)
        ingress_data = IngressData(
            session_id=data["session_id"],
            service_code=data["service_code"],
            phone_number=data["phone_number"],
            text=data["text"],
            network_code=data["network_code"]
        )
        response = ussd_service.ingress(ingress_data)
        return JsonResponse({"response": response})
    return JsonResponse({"error": "Invalid request method"}, status=400)
```

4. Add a URL pattern in `ussdapp/urls.py`:

```python
# ussdapp/urls.py

from django.urls import path
from .views import ingress

urlpatterns = [
    path("ussd/ingress", ingress, name="ingress"),
]
```

5. Include `ussdapp` URLs in the main `urls.py`:

```python
# ussdproject/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ussdapp.urls')),
]
```

### Running the Django Application

Run your Django application:

```bash
python manage.py runserver
```

## Contributing

We welcome contributions to UssdFlow! If you have suggestions, bug reports, or want to contribute code, please check our [Contributing Guidelines](./CONTRIBUTING.md).

## License

UssdFlow is licensed under the MIT License. See the [LICENSE](./LICENSE) file for more details.

By following this documentation, you should be able to integrate UssdFlow with Flask, FastAPI, and Django to create, manage, and serve USSD menus efficiently.
