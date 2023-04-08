import json


def consume_live_event(ch, method, properties, body):
    LiveEvents.add_event(message_body=json.loads(body.decode('utf-8')))
    print(f"Received message: {LiveEvents.events_list}")


class LiveEvents:
    events_list = {
        "bought_trip_id": [],
        "hotel": [],
        "destination": [],
    }

    @classmethod
    def flush_all_events(cls):
        cls.events_list["bought_trip_id"].clear()
        cls.events_list["hotel"].clear()
        cls.events_list["destination"].clear()

    @classmethod
    def add_event(cls, message_body: dict):
        for key in message_body.keys():
            cls.events_list[key].append(message_body[key])
