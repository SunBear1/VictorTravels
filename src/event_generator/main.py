import ast
import json
import logging
import os
import random
import time

from generate.generators import generate_hotel_price_change, generate_connection_price_change, \
    generate_hotel_availability_change, generate_connection_availability_change
from rabbitmq.rabbitmq_client import RabbitMQClient, RANDOM_EVENTS_PUBLISH_QUEUE_NAME, RANDOM_EVENTS_EXCHANGE_NAME

logger = logging.getLogger("event-generator")

handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
logger.setLevel(logging.INFO)
logger.addHandler(handler)

ACTIVATE_GENERATION = ast.literal_eval(os.getenv("ACTIVATE_GENERATION", "True"))
GENERATION_FREQUENCY = int(os.getenv("GENERATION_FREQUENCY", 5))

if __name__ == "__main__":
    logger.info("Random events generator started")
    event_generator_client = RabbitMQClient()

    message_id = 1
    event_generating_functions = [generate_hotel_price_change, generate_connection_price_change,
                                  generate_hotel_availability_change, generate_connection_availability_change]

    logger.info(f"Generating events mode is set to: {ACTIVATE_GENERATION}")
    while True:
        time.sleep(GENERATION_FREQUENCY)
        if not ACTIVATE_GENERATION:
            continue
        event_generation_function = random.choice(event_generating_functions)
        random_payload = event_generation_function()
        random_payload["id"] = message_id

        event_generator_client.send_data_to_queue(queue_name=RANDOM_EVENTS_PUBLISH_QUEUE_NAME,
                                                  payload=json.dumps(random_payload, ensure_ascii=False).encode(
                                                      'utf-8'),
                                                  exchange_name=RANDOM_EVENTS_EXCHANGE_NAME)
        message_id += 1
