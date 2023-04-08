import json

from fastapi import APIRouter, status
from starlette.responses import JSONResponse, Response

from common.constants import LIVE_EVENTS_QUEUE_NAME, LIVE_EVENTS_EXCHANGE_NAME
from rabbitmq.live_events import LiveEvents
from rabbitmq.rabbitmq_client import RabbitMQClient

router = APIRouter(prefix="/api/v1/events")


@router.get("",
            responses={
                200: {"description": "Events payload successfully sent"},
            },
            )
async def get_events():
    """
    Returns new event from LiveEvents list
    """
    response = JSONResponse(status_code=status.HTTP_200_OK, content=LiveEvents.events_list.copy(),
                            media_type="application/json")
    LiveEvents.flush_all_events()
    return response


@router.get("/publish",
            responses={
                200: {"description": "Events payload successfully sent"},
            },
            )
async def publish_event():
    """
    Returns new event from LiveEvents list
    """
    example_payload = {
        "bought_trip_id": ["trip_12345"],
        "hotel":
            [{
                "hotel_name": "OsovaCourt",
                "hotel_room": "small",
            }],
        "destination": [{
            "country": "Toruń",
            "transport_type": "rower"
        }]
    }
    RabbitMQClient.send_data_to_queue(queue_name=LIVE_EVENTS_QUEUE_NAME,
                                      payload=json.dumps(example_payload, ensure_ascii=False).encode('utf-8'),
                                      exchange_name=LIVE_EVENTS_EXCHANGE_NAME)
    return Response(status_code=status.HTTP_201_CREATED, content=f"elo",
                    media_type="text/plain")
