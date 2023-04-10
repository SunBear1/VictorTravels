import json
from datetime import datetime

from fastapi import APIRouter, status
from starlette.responses import JSONResponse

from mongodb.mongodb_client import MongoDBClient
from rabbitmq.rabbitmq_client import RabbitMQClient, PURCHASES_EXCHANGE_NAME, \
    RESERVATIONS_EXCHANGE_NAME, RESERVATIONS_PUBLISH_QUEUE_NAME, \
    PURCHASES_PUBLISH_QUEUE_NAME

router = APIRouter(prefix="/api/v1/reservation")


@router.post("/{trip_id}",
             responses={
                 201: {"description": "Reservation successfully created"},
                 404: {"description": "Trip with provided ID does not exist"},
                 422: {"description": "Unknown error occurred"}
             },
             )
async def make_reservation(trip_id: str):
    """
    Create a trip reservation
    """
    # TODO Czy trip jest w liście dostępnych tripów?
    current_time = datetime.now().strftime("%Y-%m-%d:%H:%M:%S")
    init_doc = {
        "trip_id": trip_id,
        "reservation_status": "temporary",
        "reservation_creation_time": current_time,
    }
    try:
        insert_result = MongoDBClient.reservations_collection.insert_one(document=init_doc)
        msg_to_purchase_ms = {
            "_id": str(insert_result.inserted_id),
            "reserved": True
        }
        client = RabbitMQClient.get_instance()
        client.send_data_to_queue(queue_name=PURCHASES_PUBLISH_QUEUE_NAME, exchange_name=PURCHASES_EXCHANGE_NAME,
                                  payload=json.dumps(msg_to_purchase_ms, ensure_ascii=False).encode('utf-8'))
        msg_to_director_ms = {
            "trip_id": trip_id,
            "reserved": True,
        }
        client.send_data_to_queue(queue_name=RESERVATIONS_PUBLISH_QUEUE_NAME, exchange_name=RESERVATIONS_EXCHANGE_NAME,
                                  payload=json.dumps(msg_to_director_ms, ensure_ascii=False).encode('utf-8'))
        # TODO wysłać wiadomość do payment MS o czasie stworzenia rezerwacji
        return JSONResponse(status_code=status.HTTP_201_CREATED,
                            content={"reservation_id": str(insert_result.inserted_id)},
                            media_type="application/json")
    except Exception as ex:  # TODO to exception będzie zmienione na bardziej konkretne kiedy powstanie reservation service
        raise ex
