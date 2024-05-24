from ussd_lib.utils import ActionRegistry

action_registry = ActionRegistry()

from . import account


__all__ = ["account"]
