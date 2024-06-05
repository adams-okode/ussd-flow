# ussd_demo/main.py
import logging
from typing import Any
from urllib.parse import parse_qs, unquote_plus

from fastapi import Body, FastAPI, Request, Response

from fastapi_demo.actions import get_action_registry
from lib.models import IngressData
from lib.router import USSDService

logger = logging.getLogger(__name__)
app = FastAPI()

# Initialize the USSDService with the action registry
action_registry = get_action_registry()
ussd_service = USSDService(
    menu_file_path="data/menu.json", actions_registry=action_registry
)


@app.api_route("/actions", methods=["GET"])
def list_actions(request: Request):
    return action_registry.get_decorated_functions_jsonable()


@app.api_route("/events", methods=["POST"])
def events(body: Any = Body(None)):
    print(body)


@app.api_route("/ussd", methods=["POST"])
async def ussd(request: Request):
    # Read and decode the request body
    body_bytes = await request.body()
    body_str = body_bytes.decode("utf-8")

    # Parse the URL-encoded data
    parsed_data = parse_qs(body_str)

    # Build the dictionary with the parsed data
    data = {
        "phone_number": unquote_plus(parsed_data.get("phoneNumber", [""])[0]),
        "service_code": unquote_plus(parsed_data.get("serviceCode", [""])[0]),
        "text": unquote_plus(parsed_data.get("text", [""])[0]),
        "session_id": unquote_plus(parsed_data.get("sessionId", [""])[0]),
        "network_code": unquote_plus(parsed_data.get("networkCode", [""])[0]),
    }

    ingress_data = IngressData(**data)

    # Call menu_level_router with the dictionary
    result = ussd_service.menu_level_router(ingress_data)

    return Response(
        content=f"{result}",
        media_type="text/plain",
    )
