import asyncio
import json

from rabbitmq.rabbitmq_client import RabbitMQClient


def start_consuming(queue_name, consume_function):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    client = RabbitMQClient.get_instance()
    loop.run_until_complete(client.start_consuming(queue_name, consume_function))


def consume_purchase_ms_event(ch, method, properties, body):
    print(f"WOW I GOT: {json.loads(body.decode('utf-8'))} FROM PURCHASE MS")


def consume_director_ms_event(ch, method, properties, body):
    print(f"WOW I GOT: {json.loads(body.decode('utf-8'))} FROM DIRECTOR MS")
