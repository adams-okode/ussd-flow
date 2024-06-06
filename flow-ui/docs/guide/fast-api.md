# UssdFlow with FastAPI

## Installation

Install FastAPI, Uvicorn, and UssdFlow using pip:

```bash
pip install fastapi uvicorn ussdflow
```

## FastAPI Application

Create a `main.py` file for your FastAPI application:

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from ussdflow import CacheManager, IngressData, USSDService

app = FastAPI()

# Initialize the cache manager
cache_manager = CacheManager(cache_type="redis", host="localhost", port=6379)

# Initialize the USSD service
ussd_service = USSDService(
    menu_file_path="path/to/your/menu.json",
    cache_manager=cache_manager
)

class USSDRequest(BaseModel):
    session_id: str
    service_code: str
    phone_number: str
    text: str
    network_code: str

@app.post("/ussd/ingress")
def ingress(request: USSDRequest):
    try:
        ingress_data = IngressData(
            session_id=request.session_id,
            service_code=request.service_code,
            phone_number=request.phone_number,
            text=request.text,
            network_code=request.network_code
        )
        response = ussd_service.ingress(ingress_data)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## Running the FastAPI Application

Run your FastAPI application:

```bash
uvicorn main:app --reload
```
