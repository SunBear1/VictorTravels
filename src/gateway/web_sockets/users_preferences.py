import logging

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from web_sockets.web_socket_manager import websocket_manager

router = APIRouter(prefix="/ws/events")

logger = logging.getLogger("gateway")


@router.websocket("/preferences")
async def send_user_preferences_event(preferences_ws: WebSocket):
    await preferences_ws.accept()

    if websocket_manager.user_preferences_client is not None:
        await preferences_ws.close()
        return

    websocket_manager.user_preferences_client = preferences_ws

    try:
        logger.info("Established connection to client via websocket on preferences endpoint.")
        while True:
            await preferences_ws.receive_text()
    except WebSocketDisconnect:
        websocket_manager.user_preferences_client = None
        logger.info("Client disconnected from websocket.")
