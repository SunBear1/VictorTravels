import logging

from fastapi import APIRouter
from starlette import status
from starlette.responses import JSONResponse, Response

from service.generated_events import get_events

router = APIRouter(prefix="/api/v1/events")

logger = logging.getLogger("gateway")


@router.get("/generated",
            responses={
                200: {"description": "Events successfully listed"},
                500: {"description": "Unknown error occurred"},
            },
            )
async def present_generated_events():
    """
    Return list of all gathered generated events
    """
    try:
        events_data = get_events()
        logger.info(f"Listing all events.")
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content=events_data,
                            media_type="application/json")
    except Exception as ex:
        logger.info(f"Exception in gateway occurred: {ex}")
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
