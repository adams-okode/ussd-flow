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

<!-- ## Documentation
Comprehensive documentation is available to guide you through the installation, configuration, and usage of UssdFlow. Check the UssdFlow Documentation for detailed information.
-->

## Contributing

We welcome contributions to UssdFlow! If you have suggestions, bug reports, or want to contribute code, please check our [Contributing Guidelines](./CONTRIBUTING.md).

## License

UssdFlow is licensed under the MIT License. See the [LICENSE](./LICENSE) file for more details.
