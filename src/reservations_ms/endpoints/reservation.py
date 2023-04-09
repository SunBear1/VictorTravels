from fastapi import APIRouter, Response, status
from mongodb.mongodb_client import MongoDBClient
from starlette.responses import JSONResponse

from rabbitmq.rabbitmq_client import RabbitMQClient, PURCHASES_QUEUE_NAME, PURCHASES_EXCHANGE_NAME, \
    RESERVATIONS_QUEUE_NAME, RESERVATIONS_EXCHANGE_NAME

router = APIRouter(prefix="/api/v1/reservation")


@router.post("/{trip_id}",
             responses={
                 201: {"description": "Reservation successfully created"},
                 403: {"description": "User does not have permission to use this service"},
                 404: {"description": "Trip with provided ID does not exist"},
                 422: {"description": "Unknown error occurred"}
             },
             )
async def make_reservation(trip_id: str):
    """
    Make a trip reservation
    """
    # TODO Czy trip jest w liście dostępnych tripów?
    init_doc = {
        "trip_id": trip_id,
        "reserved": True,
        "purchased": False,
        "payed": False
    }
    try:
        insert_result = MongoDBClient.trips_collection.insert_one(document=init_doc)
        print(MongoDBClient.trips_collection.find_one({"_id": insert_result.inserted_id}))
        msg_to_purchase_ms = {
            "_id": insert_result.inserted_id,
            "reserved": True
        }
        client = RabbitMQClient.get_instance()
        client.send_data_to_queue(queue_name=PURCHASES_QUEUE_NAME, exchange_name=PURCHASES_EXCHANGE_NAME,
                                  payload=msg_to_purchase_ms)
        msg_to_director_ms = {
            "trip_id": trip_id,
            "reserved": True,
            "payed": False
        }
        client.send_data_to_queue(queue_name=RESERVATIONS_QUEUE_NAME, exchange_name=RESERVATIONS_EXCHANGE_NAME,
                                  payload=msg_to_director_ms)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"reservation_id": insert_result.inserted_id},
                            media_type="application/json")
    except Exception:  # TODO to exception będzie zmienione na bardziej konkretne kiedy powstanie reservation service
        return Response(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=f"Something went wrong",
                        media_type="text/plain")
