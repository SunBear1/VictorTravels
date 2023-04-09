import os

import pika

USERNAME = os.getenv("RABBITMQ_USERNAME", "admin")
PASSWORD = os.getenv("RABBITMQ_PASSWORD", "admin")
VHOST = os.getenv("RABBITMQ_VHOST", "/victor_travels")
HOST = os.getenv("RABBITMQ_ADDRESS", "localhost")
PORT = os.getenv("RABBITMQ_PORT", 5672)

PURCHASES_CONSUME_QUEUE_NAME = "purchases-for-reservations-ms"
RESERVATIONS_CONSUME_QUEUE_NAME = "reservations-for-reservations-ms"

PURCHASES_EXCHANGE_NAME = "purchases"
PURCHASES_PUBLISH_QUEUE_NAME = "purchases-for-purchase_ms"
RESERVATIONS_EXCHANGE_NAME = "reservations"
RESERVATIONS_PUBLISH_QUEUE_NAME = "reservations-for-director"


class RabbitMQClient:
    __instance = None

    @staticmethod
    def get_instance():
        """Static access method to get the singleton instance."""
        if RabbitMQClient.__instance is None:
            RabbitMQClient()
        return RabbitMQClient.__instance

    def __init__(self):
        """Virtually private constructor."""
        if RabbitMQClient.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.credentials = pika.credentials.PlainCredentials(username=USERNAME, password=PASSWORD)
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=HOST, port=PORT, credentials=self.credentials, virtual_host=VHOST,
                                          heartbeat=10))
            self.channel = self.connection.channel()
            RabbitMQClient.__instance = self

    def start_consuming(self, queue_name: str, consume_function):
        self.channel.basic_consume(queue=queue_name, on_message_callback=consume_function, auto_ack=True)
        self.channel.start_consuming()

    def send_data_to_queue(self, queue_name: str, payload, exchange_name: str):
        self.channel.basic_publish(exchange=exchange_name,
                                   routing_key=queue_name,
                                   body=payload)

    def close_connection(self):
        self.connection.close()
