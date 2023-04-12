import asyncio
import json
import logging

from rabbitmq.rabbitmq_client import RabbitMQClient

logger = logging.getLogger("gateway")


def start_consuming(queue_name, consume_function):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    consumer_client = RabbitMQClient()
    loop.run_until_complete(consumer_client.start_consuming(queue_name, consume_function))
    consumer_client.close_connection()


def consume_live_event(ch, method, properties, body):
    LiveEvents.add_event(message_body=json.loads(body.decode('utf-8')))
    logger.info(msg=f"Received a message from Director MS: {body}")


class LiveEvents:
    events_list = {
        "bought_trip_id": [],
        "hotel": [],
        "destination": [],
    }

    @classmethod
    def flush_all_events(cls):
        cls.events_list["bought_trip_id"].clear()
        cls.events_list["hotel"].clear()
        cls.events_list["destination"].clear()

    @classmethod
    def add_event(cls, message_body: dict):
        for key in message_body.keys():
            cls.events_list[key].append(message_body[key])
