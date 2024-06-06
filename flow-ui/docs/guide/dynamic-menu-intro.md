# Dynamic Menus

It's important to have the ability to load menus dynamically at runtime, the reason being that making changes to dynamically served data is much easier than on statically defined menus may need recompilation and redeployment of the app.

## Menu Structure

1. **Menu Levels**
   For every request to the API, the server responds with a message, sending the user deeper into the implemented sequence hence the term levels. It's important to keep track of where the user is currently at, to know which Menu or response to serve.
2. **Menu Options**
   As the name suggests these are just options provided to the user within the Menu to allow the user to know how to respond on the USSD interface.
