# USSD Flow: Caching and USSD Session Documentation

## USSD Session

A `USSDSession` represents the current state of a user's interaction with a USSD application. It holds crucial information about the user's session, including their current position in the menu hierarchy and any additional data required to process their requests effectively.

### USSDSession Model

```python
class USSDSession(BaseModel):
    id: str
    session_id: str
    service_code: str
    phone_number: str
    text: str
    previous_menu_level: Union[int, str, None]
    current_menu_level: Union[int, str, None]
    metadata: Any
```

- **id**: Unique identifier for the session.
- **session_id**: Identifier for the USSD session, typically provided by the USSD gateway.
- **service_code**: The service code that the user dialed to access the USSD service.
- **phone_number**: The phone number of the user.
- **text**: The input text from the user.
- **previous_menu_level**: The previous menu level the user was on.
- **current_menu_level**: The current menu level the user is on.
- **metadata**: Additional data related to the session.

## Caching

Caching is a crucial aspect of the USSD Flow application, ensuring efficient session management and quick access to frequently used data. The `CacheManager` provides a unified interface for different types of caches, including Redis, PostgreSQL, and file-based caches. This allows for flexible and efficient storage and retrieval of session data.

### CacheManager

The `CacheManager` class provides a unified interface for managing different types of caches. It supports Redis, PostgreSQL, file-based caches, and custom cache objects. This flexibility allows the USSD application to adapt to various storage requirements and performance considerations.

#### Initialization

To initialize a `CacheManager`, specify the type of cache and provide any necessary configuration parameters:

```python
from ussdflow import CacheManager

# Initialize Redis cache
cache_manager = CacheManager(
    cache_type="redis",
    config={"host": "localhost", "port": 6379, "db": 0}
)

# Initialize PostgreSQL cache
cache_manager = CacheManager(
    cache_type="postgres",
    sessionmaker=your_sessionmaker_instance,
    cache_table="your_cache_table"
)

# Initialize file-based cache
cache_manager = CacheManager(
    cache_type="file",
    file_path="path/to/your/cache.json"
)

# Initialize with a custom cache object
custom_cache = YourCustomCacheImplementation()
cache_manager = CacheManager(
    cache_type="custom",
    custom_cache=custom_cache
)
```

#### Methods

- **set(key: str, value: USSDSession) -> USSDSession**:
  Stores a USSD session object in the cache.

  ```python
  session = USSDSession(
      id="unique_id",
      session_id="session_id",
      service_code="*123#",
      phone_number="254712345678",
      text="",
      previous_menu_level=None,
      current_menu_level="main_menu",
      metadata={}
  )
  cache_manager.set("session_key", session)
  ```

- **get(key: str) -> USSDSession | None**:
  Retrieves a USSD session object from the cache.

  ```python
  session = cache_manager.get("session_key")
  if session:
      print(session.phone_number)
  ```

- **delete(key: str)**:
  Deletes a USSD session object from the cache.

  ```python
  cache_manager.delete("session_key")
  ```

## Extending the Caching Manager

To extend the caching manager with a custom cache implementation, create a new class that inherits from the `Cache` abstract base class and implement the required methods (`set`, `get`, `delete`).

### Example Custom Cache

```python
class CustomCache(Cache):
    def __init__(self, custom_param):
        self.storage = {}
        self.custom_param = custom_param

    def set(self, key, value):
        self.storage[key] = value

    def get(self, key):
        return self.storage.get(key)

    def delete(self, key):
        if key in self.storage:
            del self.storage[key]

# Use the custom cache with CacheManager
custom_cache = CustomCache(custom_param="example")
cache_manager = CacheManager(
    cache_type="custom",
    custom_cache=custom_cache
)
```
