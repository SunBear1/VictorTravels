import json
import os

import pika

from rabbitmq.live_events import LiveEvents

USERNAME = os.getenv("RABBITMQ_USERNAME", "admin")
PASSWORD = os.getenv("RABBITMQ_PASSWORD", "admin")
VHOST = os.getenv("RABBITMQ_VHOST", "/victor_travels")
HOST = os.getenv("RABBITMQ_ADDRESS", "localhost")
PORT = os.getenv("RABBITMQ_PORT", 5672)


class RabbitMQClient:
    credentials = pika.credentials.PlainCredentials(username=USERNAME, password=PASSWORD)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=HOST, port=PORT, credentials=credentials, virtual_host=VHOST, heartbeat=10))
    channel = connection.channel()
    channel.queue_declare(queue='liveEventsQueue', durable=True)

    @classmethod
    async def create_connection_and_start_consuming(cls):
        def callback(ch, method, properties, body):
            LiveEvents.add_event(message_body=json.loads(body.decode('utf-8')))
            print(f"Received message: {LiveEvents.events_list}")

        cls.channel.basic_consume(queue='liveEventsQueue', on_message_callback=callback, auto_ack=True)
        cls.channel.start_consuming()

    @classmethod
    def send_data_to_queue(cls, queue_name: str, payload):
        cls.channel.basic_publish(exchange='liveEventsExchange',
                                  routing_key=queue_name,
                                  body=payload)

    @classmethod
    def close_connection(cls):
        cls.connection.close()
