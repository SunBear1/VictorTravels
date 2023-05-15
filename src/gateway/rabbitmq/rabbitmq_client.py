import logging
import os
import socket
import time

import pika

USERNAME = os.getenv("RABBITMQ_USERNAME", "admin")
PASSWORD = os.getenv("RABBITMQ_PASSWORD", "admin")
VHOST = os.getenv("RABBITMQ_VHOST", "/victor_travels")
HOST = os.getenv("RABBITMQ_ADDRESS", "localhost")
PORT = os.getenv("RABBITMQ_PORT", 5672)

logger = logging.getLogger("reservations")


class RabbitMQClient:
    def __init__(self):
        self.credentials = pika.credentials.PlainCredentials(username=USERNAME, password=PASSWORD)
        self.connection = None
        self.channel = None
        self.retry_interval = 3

        while True:
            try:
                logger.info("Connecting to RabbitMQ...")
                self.connection = pika.BlockingConnection(
                    pika.ConnectionParameters(host=HOST, port=PORT, credentials=self.credentials, virtual_host=VHOST,
                                              heartbeat=10))
                self.channel = self.connection.channel()
                if self.connection.is_open:
                    logger.info(f"Connection to RabbitMQ at {HOST}:{PORT} established.")
                    break
            except pika.exceptions.AMQPConnectionError:
                logger.info(f"Failed to establish connection to RabbitMQ")
                time.sleep(self.retry_interval)
            except socket.gaierror:
                logger.info(f"Failed to resolve RabbitMQ hostname")
                time.sleep(self.retry_interval)

    def start_consuming(self, queue_name: str, consume_function):
        self.channel.basic_consume(queue=queue_name, on_message_callback=consume_function, auto_ack=True)
        logger.info(f"Started consuming messages from queue {queue_name}")
        self.channel.start_consuming()

    def send_data_to_queue(self, queue_name: str, payload, exchange_name: str):
        try:
            logger.info(f"Sending message for queue {queue_name}")
            self.channel.basic_publish(exchange=exchange_name,
                                       routing_key=queue_name,
                                       body=payload)
        except pika.exceptions.AMQPConnectionError as e:
            print(f"Error sending message to queue {queue_name}: {e}")

    def close_connection(self):
        self.connection.close()
