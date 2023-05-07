import json
import logging
import threading

import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi.openapi.utils import get_openapi

from common.constants import LIVE_EVENTS_QUEUE_NAME
from endpoints.events import router as event_router
from endpoints.payments import router as payments_router
from endpoints.purchases import router as purchases_router
from endpoints.reservations import router as reservations_router
from endpoints.trips import router as trips_router
from endpoints.users import router as users_router
from rabbitmq.live_events import consume_live_event, start_consuming

app = FastAPI()

api_router = APIRouter()

app.include_router(users_router, tags=["Endpoints for user operations"])
app.include_router(payments_router, tags=["Endpoints for payment ms operations"])
app.include_router(purchases_router, tags=["Endpoints for purchase ms operations"])
app.include_router(reservations_router, tags=["Endpoints for reservations ms operations"])
app.include_router(trips_router, tags=["Endpoints for trip researcher operations"])
app.include_router(event_router, tags=["Endpoints for status events operations"])
app.include_router(api_router)

logger = logging.getLogger("gateway")

handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
logger.setLevel(logging.INFO)
logger.addHandler(handler)


@app.on_event("startup")
async def startup_event():
    live_events_consumer = threading.Thread(target=start_consuming,
                                            args=(LIVE_EVENTS_QUEUE_NAME, consume_live_event))
    live_events_consumer.start()


if __name__ == "__main__":
    openapi_schema = get_openapi(
        title="Dokumentacja REST API",
        version="1.0.0",
        description="Dokumentacja REST API dla wszystkich serwisów platformy VictorTravels",
        routes=app.routes,
    )
    with open("openapi.json", "w") as f:
        json.dump(openapi_schema, f)

    uvicorn.run(app, host="127.0.0.1", port=8080)
