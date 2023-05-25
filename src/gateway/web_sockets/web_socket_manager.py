import json
import logging

from fastapi import WebSocket

logger = logging.getLogger("gateway")


class WebSocketManager:
    _instance = None
    user_preferences_client: WebSocket = None
    generated_offer_change_client: WebSocket = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    async def send_message_over_websocket(self, json_body):
        # logger.info(cls.generated_offer_change_client, cls.user_preferences_client)

        msg_body = json.dumps(json_body)
        title = json_body["title"]

        if title == "user_preferences_live_event":
            client = self.user_preferences_client
            endpoint = "preferences"
        elif title == "generated_offer_change_live_event":
            client = self.generated_offer_change_client
            endpoint = "generated"
        else:
            logger.info("Unrecognized message title")
            return

        if client is not None:
            logger.info(f"Sending {msg_body} to connected {endpoint} client.")
            await client.send_text(msg_body)
        else:
            logger.info(f"There are no connected clients via {endpoint} websocket.")


websocket_manager = WebSocketManager()
