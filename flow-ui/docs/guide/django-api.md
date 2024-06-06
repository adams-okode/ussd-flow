# UssdFlow with Django

## Installation

Install Django and UssdFlow using pip:

```bash
pip install django ussdflow
```

## Django Project and Application Setup

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

## Running the Django Application

Run your Django application:

```bash
python manage.py runserver
```
