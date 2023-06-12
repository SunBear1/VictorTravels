import asyncio
import json
import logging
import os
import random

import uvicorn
from fastapi import FastAPI

from generate.generators import generate_hotel_price_change, generate_hotel_availability_change, \
    generate_connection_availability_change, generate_connection_price_change
from rabbitmq.rabbitmq_client import RabbitMQClient, RANDOM_EVENTS_PUBLISH_QUEUE_NAME, RANDOM_EVENTS_EXCHANGE_NAME

logger = logging.getLogger("event-generator")

handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
logger.setLevel(logging.INFO)
logger.addHandler(handler)
GENERATION_FREQUENCY = int(os.getenv("GENERATION_FREQUENCY", 10))

app = FastAPI()
message_id = 1
event_generating_functions = [generate_hotel_price_change, generate_connection_price_change,
                              generate_hotel_availability_change, generate_connection_availability_change]


@app.get("/api/v1/healthcheck")
def healthcheck():
    return {"status": "OK"}


def generate_random_event():
    global message_id
    event_generation_function = random.choice(event_generating_functions)
    random_payload = event_generation_function()
    random_payload["id"] = message_id
    event_generator_client = RabbitMQClient()
    event_generator_client.send_data_to_queue(queue_name=RANDOM_EVENTS_PUBLISH_QUEUE_NAME,
                                              payload=json.dumps(random_payload, ensure_ascii=False).encode(
                                                  'utf-8'),
                                              exchange_name=RANDOM_EVENTS_EXCHANGE_NAME)
    event_generator_client.close_connection()
    message_id += 1


async def run_background_task():
    while True:
        generate_random_event()
        await asyncio.sleep(GENERATION_FREQUENCY)


@app.on_event("startup")
async def startup_event():
    loop = asyncio.get_event_loop()
    loop.create_task(run_background_task())


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
