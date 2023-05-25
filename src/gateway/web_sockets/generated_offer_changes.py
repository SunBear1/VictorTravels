import logging

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from web_sockets.web_socket_manager import websocket_manager

router = APIRouter(prefix="/ws/events")

logger = logging.getLogger("gateway")


@router.websocket("/generated")
async def send_generated_offer_changing_event(generated_ws: WebSocket):
    await generated_ws.accept()

    if websocket_manager.generated_offer_change_client is not None:
        await generated_ws.close()
        return

    websocket_manager.generated_offer_change_client = generated_ws

    try:
        logger.info("Established connection to client via websocket on generated endpoint.")
        while True:
            await generated_ws.receive_text()
    except WebSocketDisconnect:
        websocket_manager.generated_offer_change_client = None
        logger.info("Client disconnected from websocket.")
