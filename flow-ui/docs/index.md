---
layout: home

hero:
  name: USSD Flow
  image:
    src: /images/default.png
    alt: USSD Flow
  actions:
    - theme: brand
      text: Get Started
      link: /guide/ussd-intro
    - theme: alt
      icon: https://github.githubassets.com/favicons/favicon.svg
      text: View on GitHub
      link: https://github.com/adams-okode/ussd-flow
---

 <Badge type="info" text="default" />

## Getting Started

You can get started using USSD Flow right away using `pip install `!

```bash
pip install ussdflow
```

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
