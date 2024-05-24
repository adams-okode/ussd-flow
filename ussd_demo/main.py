import logging
from typing import Any
from urllib.parse import parse_qs, unquote_plus

from fastapi import Body, FastAPI, Request, Response

from lib.models import IngressData
from lib.router import USSDService
from ussd_demo.actions import action_registry

logger = logging.getLogger(__name__)
app = FastAPI()
ussd_service = USSDService(actions_registry=action_registry)


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
