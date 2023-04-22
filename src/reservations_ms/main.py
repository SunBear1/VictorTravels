import logging
import threading

import uvicorn
from fastapi import FastAPI, APIRouter

from endpoints.reservation import router as reservations_router
from rabbitmq.consumers import consume_purchase_ms_event, consume_eventhub_ms_event, start_consuming
from rabbitmq.rabbitmq_client import PURCHASES_CONSUME_QUEUE_NAME, RESERVATIONS_CONSUME_QUEUE_NAME

app = FastAPI()

api_router = APIRouter()

app.include_router(reservations_router, tags=["Endpoints for reservations ms operations"])
app.include_router(api_router)

logger = logging.getLogger("reservations")

handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
logger.setLevel(logging.INFO)
logger.addHandler(handler)


@app.on_event("startup")
async def startup_event():
    purchases_consumer = threading.Thread(target=start_consuming,
                                          args=(PURCHASES_CONSUME_QUEUE_NAME, consume_purchase_ms_event))
    purchases_consumer.start()
    reservations_consumer = threading.Thread(target=start_consuming,
                                             args=(RESERVATIONS_CONSUME_QUEUE_NAME, consume_eventhub_ms_event))
    reservations_consumer.start()


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
