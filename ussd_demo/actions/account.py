from ussd_demo.actions import action_registry


@action_registry.handler()
def process_account_phone_number(**kwargs):
    return {"phone_number": "254702759950"}


@action_registry.handler()
def process_account_balance(**kwargs):
    return {"account_balance": 1000}


@action_registry.handler()
def process_account_number(**kwargs):
    return {"account_number": "123412512"}
