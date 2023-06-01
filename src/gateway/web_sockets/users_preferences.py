import logging

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from web_sockets.web_socket_manager import websocket_manager

router = APIRouter(prefix="/ws/events")

logger = logging.getLogger("gateway")


@router.websocket("/preferences")
async def send_user_preferences_event(preferences_ws: WebSocket):
    await preferences_ws.accept()

    if preferences_ws in websocket_manager.user_preferences_clients:
        await preferences_ws.close()
        return

    try:
        websocket_manager.user_preferences_clients.append(preferences_ws)
        logger.info(f"Established connection to client {preferences_ws.client.host}:{preferences_ws.client.port} via "
                    f"websocket on preferences endpoint.")
        while True:
            await preferences_ws.receive_text()
    except WebSocketDisconnect:
        websocket_manager.user_preferences_clients.remove(preferences_ws)
        logger.info(f"Client {preferences_ws.client.host}:{preferences_ws.client.port} disconnected from websocket.")
