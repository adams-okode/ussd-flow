import importlib
import inspect
import pkgutil

from ussdflow.utils import ActionRegistry

action_registry = ActionRegistry()


def get_action_registry():
    return action_registry


def import_and_register_all_modules():
    package = __package__
    for _, module_name, _ in pkgutil.iter_modules(__path__):
        module = importlib.import_module(f"{package}.{module_name}")
        for name, obj in inspect.getmembers(module, inspect.isfunction):
            if hasattr(obj, "_is_registered_action"):
                action_registry.handler(obj)


import_and_register_all_modules()
