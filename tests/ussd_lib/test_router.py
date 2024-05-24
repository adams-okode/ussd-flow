# tests/test_ussd_service.py
import pytest
from unittest.mock import patch, MagicMock
from ussd_lib.models import IngressData, USSDSession, MenuLevel, MenuOption
from ussd_lib.router import USSDService


@pytest.fixture
def mock_cache_manager():
    return MagicMock()


@pytest.fixture
def mock_action_registry():
    return MagicMock()


@pytest.fixture
def ussd_service(mock_cache_manager, mock_action_registry):
    return USSDService(
        menu_file_path="tests/data/menu.json",
        cache_manager=mock_cache_manager,
        actions_registry=mock_action_registry,
    )


def test_load_menus(ussd_service):
    menus = ussd_service.load_menus()
    assert "1" in menus
    assert isinstance(menus["1"], MenuLevel)


def test_get_or_create_session_existing(ussd_service, mock_cache_manager):
    request = IngressData(
        session_id="1234",
        service_code="*123#",
        phone_number="1234567890",
        text="",
        network_code="999999",
    )
    mock_cache_manager.get.return_value = USSDSession(
        id="1234",
        session_id="1234",
        service_code="*123#",
        phone_number="1234567890",
        text="",
        current_menu_level="1",
        previous_menu_level="1",
    )
    session = ussd_service.get_or_create_session(request)
    assert session.session_id == "1234"
    mock_cache_manager.get.assert_called_once_with("1234")
    mock_cache_manager.set.assert_called_once_with("1234", session)


def test_get_or_create_session_new(ussd_service, mock_cache_manager):
    request = IngressData(
        session_id="1234",
        service_code="*123#",
        phone_number="1234567890",
        text="",
        network_code="999999",
    )
    mock_cache_manager.get.return_value = None
    session = ussd_service.get_or_create_session(request)
    assert session.session_id == "1234"
    mock_cache_manager.get.assert_called_once_with("1234")
    mock_cache_manager.set.assert_called_once_with("1234", session)


def test_update_session_menu_level(ussd_service, mock_cache_manager):
    session = USSDSession(
        id="1234",
        session_id="1234",
        service_code="*123#",
        phone_number="1234567890",
        text="",
        current_menu_level="1",
        previous_menu_level="1",
    )
    updated_session = ussd_service.update_session_menu_level(session, "2")
    assert updated_session.current_menu_level == "2"
    mock_cache_manager.set.assert_called_once_with("1234", updated_session)


def test_ingress_valid(ussd_service):
    request = IngressData(
        session_id="1234",
        service_code="*123#",
        phone_number="1234567890",
        text="1",
        network_code="999999",
    )
    with patch.object(
        USSDService,
        "menu_level_router",
        return_value="CON What would you like to check\n1. My account\n2. My phone number",
    ):
        response = ussd_service.ingress(request)
        assert (
            response
            == "CON What would you like to check\n1. My account\n2. My phone number"
        )


def test_ingress_error(ussd_service):
    request = IngressData(
        session_id="1234",
        service_code="*123#",
        phone_number="1234567890",
        text="1",
        network_code="999999",
    )
    with patch.object(USSDService, "menu_level_router", side_effect=Exception("Error")):
        response = ussd_service.ingress(request)
        assert response == "END An error occurred: Error"


def test_menu_level_router(ussd_service, mock_cache_manager):
    request = IngressData(
        session_id="1234",
        service_code="*123#",
        phone_number="1234567890",
        text="1",
        network_code="999999",
    )
    session = USSDSession(
        id="1234",
        session_id="1234",
        service_code="*123#",
        phone_number="1234567890",
        text="",
        current_menu_level="1",
        previous_menu_level="1",
    )
    mock_cache_manager.get.return_value = session
    with patch.object(
        USSDService,
        "load_menus",
        return_value={
            "1": MenuLevel(
                id="1",
                menu_level=1,
                text="CON What would you like to check\n1. My account\n2. My phone number",
                menu_options=[
                    MenuOption(
                        type="level", response=None, next_menu_level="2", action=None
                    ),
                    MenuOption(
                        type="response",
                        response="END Your Phone Number is ${phone_number}",
                        next_menu_level=None,
                        action="process_account_phone_number",
                    ),
                ],
                max_selections=3,
            ),
            "2": MenuLevel(
                id=2,
                menu_level=2,
                text="CON Choose account information you want to view\n1. Account number\n2. Account balance",
                menu_options=[
                    MenuOption(
                        type="response",
                        response="END Your account number is ${account_number}",
                        next_menu_level=None,
                        action="process_account_number",
                    ),
                    MenuOption(
                        type="response",
                        response="END Your Account balance is ${account_balance}",
                        next_menu_level=None,
                        action="process_account_balance",
                    ),
                ],
                max_selections=3,
            ),
        },
    ):
        response = ussd_service.menu_level_router(request)
        assert response == "CON Invalid selection"


def test_process_menu_option_response(ussd_service, mock_action_registry):
    mock_function = MagicMock(return_value={"phone_number": "1234567890"})
    mock_action_registry.get_decorated_functions.return_value = {
        "process_account_phone_number": (mock_function, "mock_module"),
    }

    with patch("importlib.import_module", return_value=mock_function):
        session = USSDSession(
            id="1234",
            session_id="1234",
            service_code="*123#",
            phone_number="1234567890",
            text="",
            current_menu_level="1",
            previous_menu_level="1",
        )

        menu_option = MenuOption(
            type="response",
            response="END Your Phone Number is ${phone_number}",
            next_menu_level=None,
            action="process_account_phone_number",
        )

        response = ussd_service.process_menu_option(session, menu_option)
        assert response == "END Your Phone Number is 1234567890"


def test_process_menu_option_level(ussd_service):
    session = USSDSession(
        id="1234",
        session_id="1234",
        service_code="*123#",
        phone_number="1234567890",
        text="",
        current_menu_level="1",
        previous_menu_level="1",
    )

    menu_option = MenuOption(
        type="level", response=None, next_menu_level="2", action=None
    )

    with patch.object(
        USSDService,
        "get_menu",
        return_value="CON Choose account information you want to view\n1. Account number\n2. Account balance",
    ):
        response = ussd_service.process_menu_option(session, menu_option)
        assert (
            response
            == "CON Choose account information you want to view\n1. Account number\n2. Account balance"
        )
