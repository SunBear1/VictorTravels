import logging
import threading

import uvicorn
from fastapi import FastAPI, APIRouter

from endpoints.purchases import router as purchase_router
from mongodb.mongodb_client import MongoDBClient
from rabbitmq.consumers import start_consuming, consume_payment_ms_event, consume_reservation_ms_event
from rabbitmq.rabbitmq_client import PURCHASES_CONSUME_QUEUE_NAME, PAYMENTS_CONSUME_QUEUE_NAME

app = FastAPI()

api_router = APIRouter()

app.include_router(purchase_router, tags=["Endpoints for purchase ms operations"])
app.include_router(api_router)

logger = logging.getLogger("purchases")

handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
logger.setLevel(logging.INFO)
logger.addHandler(handler)


@app.on_event("startup")
async def startup_event():
    MongoDBClient.connect_to_database()
    purchases_consumer = threading.Thread(target=start_consuming,
                                          args=(PURCHASES_CONSUME_QUEUE_NAME, consume_reservation_ms_event))
    purchases_consumer.start()
    reservations_consumer = threading.Thread(target=start_consuming,
                                             args=(PAYMENTS_CONSUME_QUEUE_NAME, consume_payment_ms_event))
    reservations_consumer.start()


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8002)
