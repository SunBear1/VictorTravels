import logging

from rabbitmq.consumers import start_consuming, consume_eventhub_ms_event
from rabbitmq.rabbitmq_client import TRANSPORT_CONSUME_QUEUE_NAME

logger = logging.getLogger("transports")

handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
logger.setLevel(logging.INFO)
logger.addHandler(handler)

if __name__ == "__main__":
    start_consuming(queue_name=TRANSPORT_CONSUME_QUEUE_NAME, consume_function=consume_eventhub_ms_event)
