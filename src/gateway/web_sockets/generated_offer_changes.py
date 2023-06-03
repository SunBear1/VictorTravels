import logging

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from web_sockets.web_socket_manager import websocket_manager

router = APIRouter(prefix="/ws/events")

logger = logging.getLogger("gateway")


@router.websocket("/generated")
async def send_generated_offer_changing_event(generated_ws: WebSocket):
    await generated_ws.accept()

    if generated_ws in websocket_manager.generated_offer_change_clients:
        await generated_ws.close()
        return

    try:
        websocket_manager.generated_offer_change_clients.append(generated_ws)
        logger.info(f"Established connection to client {generated_ws.client.host}:{generated_ws.client.port} via "
                    f"websocket on generated endpoint.")
        while True:
            await generated_ws.receive_text()
    except WebSocketDisconnect:
        websocket_manager.generated_offer_change_clients.remove(generated_ws)
        logger.info(f"Client {generated_ws.client.host}:{generated_ws.client.port} disconnected from websocket.")
