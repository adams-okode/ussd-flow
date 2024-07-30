from urllib.parse import parse_qs, unquote_plus

from flask import Flask, Response, request
from ussdflow import IngressData, USSDService

app = Flask(__name__)

# Initialize the cache manager
# cache_manager = CacheManager(cache_type="redis", host="localhost", port=6379)

# Initialize the USSD service
ussd_service = USSDService(menu_file_path="data/menu.json")


@app.route("/ussd", methods=["POST"])
def ingress():
    print("Starting ingress")
    # Read and decode the request body
    body_bytes = request.data
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

    # Create the IngressData object
    ingress_data = IngressData(
        session_id=data["session_id"],
        service_code=data["service_code"],
        phone_number=data["phone_number"],
        text=data["text"],
        network_code=data["network_code"],
    )

    # Process the USSD request
    response = ussd_service.ingress(ingress_data)

    # Return the response as plain text
    return Response(response, content_type="text/plain")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8000)
