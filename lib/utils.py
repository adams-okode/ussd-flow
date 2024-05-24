import inspect
from typing import Callable, Dict, Tuple


class ActionRegistry:
    def __init__(self, package_name: str = None):
        self._package_name = package_name
        self._registry: Dict[str, Tuple[Callable, str]] = {}

    def handler(self) -> Callable:
        """
        Decorator to register a function with a specific handler value.
        :return: The decorator function.
        """

        def decorator(func: Callable) -> Callable:
            module_name = inspect.getmodule(func).__name__
            self._registry[func.__name__] = (func, module_name)
            return func

        return decorator

    def get_decorated_functions(self) -> Dict[str, Tuple[Callable, str]]:
        """
        Get the registered handler functions.
        :return: Dictionary of registered handler functions with their module names.
        """
        return self._registry
