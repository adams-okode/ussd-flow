import inspect
from typing import Any, Callable, Dict, Tuple


class ActionRegistry:
    def __init__(self, package_name: str = None):
        self._package_name = package_name
        self._registry: Dict[str, Tuple[Callable, str]] = {}

    def handler(self, func: Callable = None) -> Callable:
        """
        Decorator to register a function with the action registry.
        :return: The decorator function.
        """
        if func is None:

            def wrapper(func: Callable):
                self._register_function(func)
                return func

            return wrapper
        else:
            self._register_function(func)
            return func

    def _register_function(self, func: Callable):
        module_name = inspect.getmodule(func).__name__
        self._registry[func.__name__] = (func, module_name)

    def register_function(self, func_name: str, func: Callable):
        module_name = inspect.getmodule(func).__name__
        self._registry[func_name] = (func, module_name)

    def get_decorated_functions(self) -> Dict[str, Tuple[Callable, str]]:
        """
        Get the registered handler functions.
        :return: Dictionary of registered handler functions with their module names.
        """
        return self._registry

    def get_decorated_functions_jsonable(self) -> Any:
        """
        Get the registered handler functions in a JSON-compatible format.
        :return: List of dictionaries with function names and module names.
        """
        return [
            {"function_name": name, "module_name": module}
            for name, (_, module) in self._registry.items()
        ]


action_registry = ActionRegistry()
