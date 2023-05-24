import asyncio
import json
import logging

from websocket import create_connection

from common.constants import WEB_GUI_ADDRESS
from rabbitmq.rabbitmq_client import RabbitMQClient

logger = logging.getLogger("gateway")


def send_message_via_websocket(channel: str, message: dict):
    ws = create_connection(f"ws://{WEB_GUI_ADDRESS}")
    ws.send(json.dumps({'channel': channel, 'message': message}))
    ws.close()


def start_consuming(queue_name, consume_function):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    consumer_client = RabbitMQClient()
    loop.run_until_complete(consumer_client.start_consuming(queue_name, consume_function))
    consumer_client.close_connection()


def consume_live_event(ch, method, properties, body):
    json_body = json.loads(body.decode("utf-8"))
    logger.info(msg=f"Received a message from EventHub MS: {json_body}")
    send_message_via_websocket(channel="related_trips", message={"trip_id": json_body["tripID"]})
    send_message_via_websocket(channel="trip_locations",
                               message={"country": json_body["country"], "region": json_body["region"]})
    send_message_via_websocket(channel="trip_details",
                               message={"hotel_name": json_body["hotelName"], "room_type": json_body["roomType"],
                                        "transport_type": json_body["transportType"]})
