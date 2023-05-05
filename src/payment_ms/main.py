import logging
import threading
import uvicorn
from fastapi import FastAPI, APIRouter

from endpoints.payments import router as payment_router
from rabbitmq.consumers import start_consuming, consume_reservations_ms_event
from rabbitmq.rabbitmq_client import PAYMENTS_CONSUME_QUEUE_NAME

app = FastAPI()

api_router = APIRouter()

app.include_router(payment_router, tags=["Endpoints for payment ms operations"])
app.include_router(api_router)

logger = logging.getLogger("payments")

handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
logger.setLevel(logging.INFO)
logger.addHandler(handler)


@app.on_event("startup")
async def startup_event():
    payments_consumer = threading.Thread(target=start_consuming,
                                         args=(PAYMENTS_CONSUME_QUEUE_NAME, consume_reservations_ms_event))
    payments_consumer.start()


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8003)
