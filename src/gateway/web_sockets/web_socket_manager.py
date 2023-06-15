import json
import logging
from typing import List

from fastapi import WebSocket

logger = logging.getLogger("gateway")


class WebSocketManager:
    _instance = None
    user_preferences_clients: List[WebSocket] = []

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    async def send_message_over_websocket(self, json_body):
        msg_body = json.dumps(json_body, ensure_ascii=False)
        title = json_body["title"]

        if title == "user_preferences_live_event":
            connected_clients = self.user_preferences_clients
            endpoint = "preferences"
        else:
            logger.info("Unrecognized message title")
            return

        for client in connected_clients:
            logger.info(f"Sending {msg_body} to connected {endpoint} client {client.client.host}:{client.client.port}.")
            await client.send_text(msg_body)


websocket_manager = WebSocketManager()
