import json
import logging

import requests
from common.authentication import oauth2_scheme, verify_jwt_token
from common.constants import PAYMENT_MS_ADDRESS
from fastapi import APIRouter, Response, Depends, status
from starlette.responses import JSONResponse
from users.service import verify_user_identify

router = APIRouter(prefix="/api/v1/payments")

logger = logging.getLogger("gateway")


@router.post("/{reservation_id}",
             responses={
                 200: {"description": "Payment performed successfully"},
                 404: {"description": "Reservation with provided ID does not exist"},
                 403: {"description": "User does not have permission to use this service"},
                 400: {"description": "Reservation with provided ID has already been paid for"},
                 410: {"description": "Reservation with ID has expired"},
                 402: {"description": "Payment for reservation have failed"},
                 500: {"description": "Unknown error occurred"}
             },
             )
async def buy_trip(reservation_id: str, token: str = Depends(oauth2_scheme)):
    """
    Pay for a specific trip
    """
    try:
        users_credentials = verify_jwt_token(token=token)
        if not verify_user_identify(login=users_credentials["login"], password=users_credentials["password"]):
            return Response(status_code=status.HTTP_403_FORBIDDEN,
                            content="User does not have permission to use this service", media_type="text/plain")

        response = requests.post(f"http://{PAYMENT_MS_ADDRESS}/api/v1/payment/{reservation_id}",
                                 timeout=3.00,
                                 verify=False)
        logger.info(f"Request redirected to {PAYMENT_MS_ADDRESS}.")

        if response.status_code == status.HTTP_200_OK:
            return JSONResponse(status_code=status.HTTP_200_OK,
                                content=json.loads(response.content.decode("utf-8")),
                                media_type="application/json")
        if response.status_code in [status.HTTP_400_BAD_REQUEST, status.HTTP_402_PAYMENT_REQUIRED,
                                    status.HTTP_404_NOT_FOUND, status.HTTP_410_GONE]:
            return Response(status_code=response.status_code,
                            content=response.content,
                            media_type="text/plain")
        if response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
            return Response(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content="Payment service crashed :-)",
                            media_type="text/plain")

    except requests.exceptions.ConnectionError:
        return Response(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content="Can't connect to payment service",
                        media_type="text/plain")
    except Exception as ex:
        logger.info(f"Exception in gateway occurred: {ex}")
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
