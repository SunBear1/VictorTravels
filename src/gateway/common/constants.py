# RabbitMQ constants
import os

LIVE_EVENTS_EXCHANGE_NAME = "live-events"
LIVE_EVENTS_QUEUE_NAME = "live-events-for-gateway"

# Other MS Addresses
TRIP_RESEARCHER_SERVICE_ADDRESS = os.getenv("TRIP_RESEARCHER_ADDRESS", "localhost:8000")
RESERVATIONS_MS_ADDRESS = os.getenv("RESERVATIONS_MS_ADDRESS", "localhost:8001")
PAYMENT_MS_ADDRESS = os.getenv("PAYMENT_MS_ADDRESS", "localhost:8002")
PURCHASE_MS_ADDRESS = os.getenv("PURCHASE_MS_ADDRESS", "localhost:8003")
WEB_GUI_ADDRESS = os.getenv("WEB_GUI_ADDRESS", "localhost:18005")
