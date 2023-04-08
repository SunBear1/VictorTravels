import os

import pika

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

    @classmethod
    async def create_connection_and_start_consuming(cls, queue_name: str, consume_function):
        cls.channel.basic_consume(queue=queue_name, on_message_callback=consume_function, auto_ack=True)
        cls.channel.start_consuming()

    @classmethod
    def send_data_to_queue(cls, queue_name: str, payload, exchange_name: str):
        cls.channel.basic_publish(exchange=exchange_name,
                                  routing_key=queue_name,
                                  body=payload)

    @classmethod
    def close_connection(cls):
        cls.connection.close()
