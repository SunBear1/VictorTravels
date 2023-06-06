import asyncio
import json
import logging
from datetime import datetime

from fastapi import APIRouter, status
from pydantic import BaseModel
from starlette.responses import JSONResponse, Response

from mongodb.mongodb_client import MongoDBClient
from rabbitmq.rabbitmq_client import RabbitMQClient, PURCHASES_EXCHANGE_NAME, \
    RESERVATIONS_EXCHANGE_NAME, RESERVATIONS_PUBLISH_QUEUE_NAME, \
    PURCHASES_PUBLISH_QUEUE_NAME, PAYMENTS_PUBLISH_QUEUE_NAME, PAYMENTS_EXCHANGE_NAME
from service.expiration_handler import start_measuring_reservation_time
from service.trip_offers_handler import check_if_hotel_exists, check_if_connection_exists, check_if_rooms_available, \
    check_if_connection_available, update_rooms_available, update_seats_available, check_if_trip_offer_exists

router = APIRouter(prefix="/api/v1/reservation")

logger = logging.getLogger("reservations")


class TripReservationData(BaseModel):
    hotel_id: str
    room_type: str
    connection_id_to: str
    connection_id_from: str
    head_count: int
    price: float


@router.post("/{trip_offer_id}",
             responses={
                 201: {"description": "Reservation successfully created"},
                 400: {"description": "Trip with provided ID does not have enough places left"},
                 404: {"description": "Trip with provided ID does not exist"},
                 500: {"description": "Unknown error occurred"}
             },
             )
async def make_reservation(trip_offer_id: str, payload: TripReservationData):
    """
    Create a trip reservation
    """
    current_os_time = datetime.now()
    current_datetime = current_os_time.strftime("%Y-%m-%dT%H:%M:%S.%f")
    try:
        if not check_if_trip_offer_exists(trip_offer_id=trip_offer_id):
            return Response(status_code=status.HTTP_404_NOT_FOUND,
                            content=f"Trip offer with ID {trip_offer_id} does not exist",
                            media_type="text/plain")
        if not check_if_hotel_exists(hotel_id=payload.hotel_id):
            return Response(status_code=status.HTTP_404_NOT_FOUND,
                            content=f"Hotel with ID {payload.hotel_id} does not exist",
                            media_type="text/plain")
        if not check_if_rooms_available(hotel_id=payload.hotel_id, room_type=payload.room_type, rooms=1):
            return Response(status_code=status.HTTP_400_BAD_REQUEST,
                            content=f"Hotel with ID {payload.hotel_id} has not enough {payload.room_type} rooms left",
                            media_type="text/plain")

        number_of_seats_to_update = -payload.head_count
        if payload.connection_id_to != "own":
            if not check_if_connection_exists(connection_id=payload.connection_id_to):
                return Response(status_code=status.HTTP_404_NOT_FOUND,
                                content=f"Connection with ID {payload.connection_id_to} does not exist",
                                media_type="text/plain")
            if not check_if_connection_available(connection_id=payload.connection_id_to, seats=payload.head_count):
                return Response(status_code=status.HTTP_400_BAD_REQUEST,
                                content=f"Connection with ID {payload.connection_id_to} has not enough seats left",
                                media_type="text/plain")
            update_seats_available(connection_id=payload.connection_id_to, value=number_of_seats_to_update)

        if payload.connection_id_from != "own":
            if not check_if_connection_exists(connection_id=payload.connection_id_from):
                return Response(status_code=status.HTTP_404_NOT_FOUND,
                                content=f"Connection with ID {payload.connection_id_from} does not exist",
                                media_type="text/plain")
            if not check_if_connection_available(connection_id=payload.connection_id_from, seats=payload.head_count):
                return Response(status_code=status.HTTP_400_BAD_REQUEST,
                                content=f"Connection with ID {payload.connection_id_from} has not enough seats left",
                                media_type="text/plain")
            update_seats_available(connection_id=payload.connection_id_from, value=number_of_seats_to_update)

        logger.info(f"Reservation creation process for offer {trip_offer_id} started at {current_datetime}")
        init_doc = {
            "trip_offer_id": trip_offer_id,
            "reservation_status": "temporary",
            "reservation_creation_time": current_datetime,
            "uid": "example_uid",
            "head_count": payload.head_count
        }
        insert_result = MongoDBClient.reservations_collection.insert_one(document=init_doc)
        reservation_id = str(insert_result.inserted_id)

        number_of_rooms_to_update = -1
        update_rooms_available(hotel_id=payload.hotel_id, room_type=payload.room_type, value=number_of_rooms_to_update)

        expiration_timer_task = asyncio.create_task(start_measuring_reservation_time(
            reservation_id=reservation_id,
            reservation_creation_time=current_datetime,
            hotel_id=payload.hotel_id,
            room_type=payload.room_type,
            connections_id=(payload.connection_id_to, payload.connection_id_from),
            head_count=payload.head_count
        ))

        client = RabbitMQClient()
        client.send_data_to_queue(queue_name=PURCHASES_PUBLISH_QUEUE_NAME,
                                  exchange_name=PURCHASES_EXCHANGE_NAME,
                                  payload=json.dumps({
                                      "title": "reservation_creation",
                                      "_id": reservation_id,
                                      "trip_offer_id": trip_offer_id,
                                      "price": payload.price
                                  }, ensure_ascii=False).encode('utf-8'))

        client.send_data_to_queue(queue_name=RESERVATIONS_PUBLISH_QUEUE_NAME,
                                  exchange_name=RESERVATIONS_EXCHANGE_NAME,
                                  payload=json.dumps({
                                      "title": "reservation_status_update",
                                      "trip_offer_id": trip_offer_id,
                                      "reservation_id": reservation_id,
                                      "reservation_status": "created",
                                      "hotel_id": payload.hotel_id,
                                      "room_type": payload.room_type,
                                      "connection_id_to": payload.connection_id_to,
                                      "connection_id_from": payload.connection_id_from,
                                      "head_count": payload.head_count
                                  }, ensure_ascii=False).encode('utf-8'))

        client.send_data_to_queue(queue_name=PAYMENTS_PUBLISH_QUEUE_NAME, exchange_name=PAYMENTS_EXCHANGE_NAME,
                                  payload=json.dumps({
                                      "title": "reservation_creation_time",
                                      "_id": reservation_id,
                                      "reservation_creation_time": current_datetime,
                                      "price": payload.price
                                  }, ensure_ascii=False).encode('utf-8'))
        client.close_connection()

        logger.info(f"Reservation with ID {reservation_id} created.")
        return JSONResponse(status_code=status.HTTP_201_CREATED,
                            content={"reservation_id": reservation_id},
                            media_type="application/json")
    except Exception as ex:
        logger.info(f"Exception in reservation ms occurred: {ex}")
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
