import importlib
import json
from typing import Any, Dict

from lib.cache import CacheManager
from lib.models import IngressData, MenuLevel, MenuOption, USSDSession
from lib.utils import ActionRegistry


class USSDService:
    def __init__(
        self,
        menu_file_path: str = "data/sample.json",
        cache_manager: CacheManager = CacheManager(cache_type="file"),
        actions_registry: ActionRegistry = ActionRegistry(),
        db_context: Any = None,  # Add db_context parameter
    ):
        """
        Initialize the USSDService with menu file path, cache manager,
        actions registry,
        and database context.

        :param menu_file_path: Path to the JSON file containing menu definitions.
        :param cache_manager: CacheManager instance for session management.
        :param actions_registry: ActionRegistry instance for action handling.
        :param db_context: Database context to be passed to action functions.
        """
        self.menu_file_path = menu_file_path
        self._cache_manager = cache_manager
        self._action_registry = actions_registry
        self._db_context = db_context  # Store db_context
        self._ussd_session = {}

    def load_menus(self) -> Dict[str, MenuLevel]:
        """
        Load menus from a JSON file.

        :return: Dictionary of menu levels.
        """
        with open(self.menu_file_path, "r") as file:
            content = file.read()
        menu_dict = json.loads(content)
        return {key: MenuLevel(**value) for key, value in menu_dict.items()}

    def get_or_create_session(self, request: IngressData) -> USSDSession:
        """
        Get an existing session or create a new one if it doesn't exist.

        :param request: IngressData object containing request information.
        :return: USSDSession object.
        """
        session_data = self._cache_manager.get(request.session_id)
        if session_data:
            session_data.text = request.text
            self._cache_manager.set(request.session_id, session_data)
            return session_data

        session_data = USSDSession(
            id=request.session_id,
            session_id=request.session_id,
            service_code=request.service_code,
            phone_number=request.phone_number,
            text=request.text,
            current_menu_level="1",
            previous_menu_level="1",
        )
        self._cache_manager.set(request.session_id, session_data)
        return session_data

    def update_session_menu_level(
        self, session: USSDSession, menu_level: str
    ) -> USSDSession:
        """
        Update the menu level of the session.

        :param session: USSDSession object.
        :param menu_level: New menu level.
        :return: Updated USSDSession object.
        """
        session.previous_menu_level = session.current_menu_level
        session.current_menu_level = menu_level
        self._cache_manager.set(session.session_id, session)
        return session

    def ingress(self, request: IngressData) -> str:
        """
        Handle an incoming USSD request.

        :param request: IngressData object containing request information.
        :return: Response string to be sent back to the user.
        """
        try:
            return self.menu_level_router(request)
        except Exception as e:
            return f"END An error occurred: {str(e)}"

    def menu_level_router(self, request: IngressData) -> str:
        """
        Route the request to the appropriate menu level.

        :param request: IngressData object containing request information.
        :return: Response string to be sent back to the user.
        """
        menus = self.load_menus()
        session = self.get_or_create_session(request)

        if request.text:
            return self.get_next_menu_item(session, menus)
        else:
            con_end = menus[session.current_menu_level].con_end
            return "{} {}".format(
                "CON" if con_end else "END", menus[session.current_menu_level].text
            )

    def get_next_menu_item(
        self, session: USSDSession, menus: Dict[str, MenuLevel]
    ) -> str:
        """
        Get the next menu item based on the user's input.

        :param session: USSDSession object.
        :param menus: Dictionary of menu levels.
        :return: Response string to be sent back to the user.
        """
        levels = session.text.split("*")
        last_value = levels[-1]
        menu_level = menus.get(str(session.current_menu_level))

        if not menu_level:
            raise Exception("Invalid menu level")

        if int(last_value) <= menu_level.max_selections:
            menu_option = menu_level.menu_options[int(last_value) - 1]
            return self.process_menu_option(session, menu_option)

        return "CON Invalid selection"

    def process_menu_option(self, session: USSDSession, menu_option: MenuOption) -> str:
        """
        Process the selected menu option.

        :param session: USSDSession object.
        :param menu_option: MenuOption object selected by the user.
        :return: Response string to be sent back to the user.
        """
        if menu_option.type == "response":
            return self.process_menu_option_responses(session, menu_option)
        elif menu_option.type == "level":
            self.update_session_menu_level(session, menu_option.next_menu_level)
            return self.get_menu(menu_option.next_menu_level)
        else:
            return "CON Invalid menu option"

    def get_menu(self, menu_level: str) -> str:
        """
        Get the text of the specified menu level.

        :param menu_level: Menu level to retrieve.
        :return: Text of the specified menu level.
        """
        menus = self.load_menus()
        con_end = menus[str(menu_level)].con_end

        return "{} {}".format(
            "CON" if con_end else "END",
            menus[str(menu_level)].text,
        )

    def process_menu_option_responses(
        self, session: USSDSession, menu_option: MenuOption
    ) -> str:
        """
        Process the responses for the selected menu option.

        :param session: USSDSession object.
        :param menu_option: MenuOption object selected by the user.
        :return: Response string to be sent back to the user.
        """
        variables_map = {}
        response = menu_option.response
        con_end = menu_option.con_end

        functions = self._action_registry.get_decorated_functions()

        if menu_option.action in functions:
            func, module_name = functions[menu_option.action]

            # Dynamically import the module containing the function
            module = importlib.import_module(module_name)

            # Get the function from the module
            func_to_call = getattr(module, menu_option.action)

            # Call the function with provided arguments
            variables_map = func_to_call(session, self._db_context)

        else:
            raise Exception(f"Function '{menu_option.action}' is not registered.")

        return "{} {}".format(
            "CON" if con_end else "END",
            self.replace_variable(variables_map, response),
        )

    @staticmethod
    def replace_variable(variables_map: Dict[str, str], response: str) -> str:
        """
        Replace variables in the response string with their actual values.

        :param variables_map: Dictionary of variable names and their values.
        :param response: Response string with placeholders.
        :return: Response string with placeholders replaced by actual values.
        """
        for key, value in variables_map.items():
            response = response.replace(f"${{{key}}}", str(value))
        return response
