# What are Actions?

Actions are predefined operations that handle various tasks within a USSD session. They can include operations such as checking a user's account balance, transferring funds, retrieving information from a database, or any other task that needs to be performed based on the user's input.

## Key Characteristics of Actions:

1. **Functionality**:

   - Actions encapsulate the logic required to perform specific tasks.
   - They are typically defined as functions that take the current session data as input and return a response that will be sent back to the user.

2. **Modularity**:

   - Actions are modular, meaning they can be defined, tested, and reused independently.
   - This modularity makes it easier to manage and extend the functionality of the USSD application.

3. **Integration**:
   - Actions are registered with the action registry, which maps action names to their corresponding functions.
   - This mapping allows the USSD flow to trigger the appropriate action based on the user’s selection in the USSD menu.

# Example of Defining and Registering Actions:

## 1. Define Actions:

Define the functions that represent the actions in your application. For example:

```python
def check_balance(session: USSDSession):
    # Logic to check the user's account balance
    return {**session}
```

## 2. Register Actions:

Register these actions with the action registry to make them available for use in the USSD flow.

```python
from ussdflow import ActionRegistry

# Create an instance of the action registry
action_registry = ActionRegistry()

# Register the actions
action_registry.register_action('check_balance', check_balance)
action_registry.register_action('transfer_funds', transfer_funds)
```

## 3. Use Actions in USSD Menus:

Define your USSD menu structure and link the actions to specific menu options.

```json
{
  "menus": {
    "main_menu": {
      "text": "Welcome to USSD Service\n1. Check Balance\n2. Transfer Funds",
      "options": {
        "1": {
          "action": "check_balance"
        },
        "2": {
          "action": "transfer_funds"
        }
      }
    }
  }
}
```

# How Actions Work in USSD Flow:

1. **User Input**:
   - The user navigates through the USSD menu and makes a selection.
2. **Action Trigger**:
   - Based on the user’s selection, the corresponding action is triggered by looking up the action registry.
3. **Action Execution**:
   - The action performs its task, such as querying a database or processing a transaction.
4. **Response Generation**:
   - The action returns a response message that is sent back to the user, completing the interaction.

## Benefits of Using Actions:

- **Scalability**: Easily add new functionalities by defining new actions.
- **Maintainability**: Manage and update individual actions without affecting other parts of the application.
- **Reusability**: Reuse common actions across different parts of the USSD application.
