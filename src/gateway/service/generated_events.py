from sql.postgresql_client import PostgreSQLClient


def save_event(event: dict):
    _id: int = event["id"]
    title: str = event["title"]
    type: str = event["type"]
    name: str = event["name"]
    if "field" in event:
        field: str = event["field"]
    else:
        field: str = ""
    resource: str = event["resource"]
    value: int = event["value"]
    operation: str = event["operation"]

    pg_client = PostgreSQLClient()
    pg_client.execute_query_for_database(
        query=f"INSERT INTO GeneratedEvents (id, title, type, name, field, resource, value, operation) VALUES ({_id}, '{title}', '{type}', '{name}', '{field}', '{resource}', {value}, '{operation}');",
        fetch_data=False)


def get_events() -> list[dict]:
    pg_client = PostgreSQLClient()
    query_result = pg_client.execute_query_for_database(
        query="SELECT id, title, type, name, field, resource, value, operation FROM GeneratedEvents;")
    events_data = []
    for event in query_result:
        event_data = {
            "id": event[0],
            "title": event[1],
            "type": event[2],
            "name": event[3],
            "field": event[4],
            "resource": event[5],
            "value": event[6],
            "operation": event[7]
        }
        events_data.append(event_data)
    return events_data
