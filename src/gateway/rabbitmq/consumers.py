import asyncio
import json
import logging

from rabbitmq.rabbitmq_client import RabbitMQClient
from web_sockets.web_socket_manager import websocket_manager

logger = logging.getLogger("gateway")


def start_consuming(queue_name, consume_function):
    consumer_client = RabbitMQClient()
    asyncio.run(consumer_client.start_consuming(queue_name, consume_function))
    consumer_client.close_connection()


def consume_live_event(ch, method, properties, body):
    json_body = json.loads(body.decode("utf-8"))
    logger.info(msg=f"Received a message from EventHub MS: {json_body}")
    asyncio.run(websocket_manager.send_message_over_websocket(json_body))