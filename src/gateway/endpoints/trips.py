from datetime import date
from typing import Optional

import requests
from fastapi import APIRouter, Response, Depends, status, Query
from starlette.responses import JSONResponse

from common.authentication import oauth2_scheme, verify_jwt_token
from common.constants import TRIP_RESEARCHER_SERVICE_ADDRESS
from users.service import verify_user_identify

router = APIRouter(prefix="/api/v1/trips")


@router.get("/{trip_id}",
            responses={
                200: {"description": "Trip's data successfully listed"},
                403: {"description": "User does not have permission to use this service"},
                404: {"description": "Trip with provided ID does not exist"},
                422: {"description": "Unknown error occurred"}
            },
            )
async def get_trip(trip_id: str, token: str = Depends(oauth2_scheme)):
    """
    Return information about specific trip
    """
    try:
        users_credentials = verify_jwt_token(token=token)
        if not verify_user_identify(login=users_credentials["login"], password=users_credentials["password"]):
            return Response(status_code=status.HTTP_403_FORBIDDEN,
                            content="User does not have permission to use this service", media_type="text/plain")

        response = requests.get(TRIP_RESEARCHER_SERVICE_ADDRESS, params={"trip_id": trip_id}, timeout=3.00,
                                verify=False)

        if response.status_code == status.HTTP_200_OK:
            return JSONResponse(status_code=status.HTTP_200_OK, content=response.content, media_type="application/json")
        if response.status_code == status.HTTP_404_NOT_FOUND:
            return Response(status_code=status.HTTP_404_NOT_FOUND, content=f"Trip with ID {trip_id} does not exist",
                            media_type="text/plain")
        if response.status_code == status.HTTP_500_INTERNAL_SERVER_ERRO:
            return Response(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content="Tour researcher crashed :-)",
                            media_type="text/plain")

    except requests.exceptions.ConnectionError:
        return Response(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content="Can't connect to tour researcher",
                        media_type="text/plain")
    except Exception:  # TODO to exception będzie zmienione na bardziej konkretne kiedy powstanie trip_researcher
        return Response(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=f"Something went wrong",
                        media_type="text/plain")


@router.get("/",
            responses={
                200: {"description": "Trips fetched successfully"},
                403: {"description": "User does not have permission to use this service"},
                400: {"description": "Invalid tour researcher query parameters"},
                422: {"description": "Unknown error occurred"}
            },
            )
async def get_trips(
        adults: Optional[int] = Query(None, gt=0),
        kids_to_3yo: Optional[int] = Query(None, ge=0),
        kids_to_10yo: Optional[int] = Query(None, ge=0),
        kids_to_18yo: Optional[int] = Query(None, ge=0),
        date_from: Optional[date] = Query(None),
        date_to: Optional[date] = Query(None),
        departure_region: Optional[str] = Query(None),
        arrival_region: Optional[str] = Query(None),
        transport: Optional[str] = Query(None),
        order: Optional[str] = Query(None),
        diet: Optional[str] = Query(None),
        max_price: Optional[int] = Query(None, gt=0),
        token: str = Depends(oauth2_scheme)
):
    try:
        users_credentials = verify_jwt_token(token=token)
        if not verify_user_identify(login=users_credentials["login"], password=users_credentials["password"]):
            return Response(status_code=status.HTTP_403_FORBIDDEN,
                            content="User does not have permission to use this service", media_type="text/plain")

        query_params = {
            "adults": adults,
            "kidsTo3yo": kids_to_3yo,
            "kidsTo10yo": kids_to_10yo,
            "kidsTo18yo": kids_to_18yo,
            "date-from": date_from,
            "date-to": date_to,
            "departure-region": departure_region,
            "arrival-region": arrival_region,
            "transport": transport,
            "order": order,
            "diet": diet,
            "max-price": max_price
        }
        response = requests.get(TRIP_RESEARCHER_SERVICE_ADDRESS, params=query_params, timeout=3.00,
                                verify=False)

        if response.status_code == status.HTTP_200_OK:
            return JSONResponse(status_code=status.HTTP_200_OK, content=response.content, media_type="application/json")
        if response.status_code == status.HTTP_400_BAD_REQUEST:
            return Response(status_code=status.HTTP_400_BAD_REQUEST, content="Query for tour researcher is invalid",
                            media_type="text/plain")
        if response.status_code == status.HTTP_500_INTERNAL_SERVER_ERRO:
            return Response(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content="Tour researcher crashed :-)",
                            media_type="text/plain")

    except Exception:  # TODO to exception będzie zmienione na bardziej konkretne kiedy powstanie trip_researcher
        return Response(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=f"Something went wrong",
                        media_type="text/plain")
