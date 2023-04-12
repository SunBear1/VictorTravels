# Design endpointów

## WEB_UI

#### AMQP Live events

```json
{
    "placeholder" : "example"
}
```

## Tour Researcher

#### Rest

`GET /api/v1/trips?`

Jeśli jakiegoś paramu nie ma to zakładamy że dowolny

Params:

- adults : number
- kidsTo3yo : number
- kidsTo10yo : number
- kidsTo18yo : number
- date-from : date
- date-to : date
- departure-region : string
- arrival-region : string
- transport : string
- order : string
- diet : string
- max-price : int

`GET /api/v1/trips/{trip_id}`

#### AMQP

```
CRUD wycieczkowy
```

## Director

TBD

## Gateway

#### Rest

`POST /api/v1/users/login`

`POST /api/v1/users/register`

`GET /api/v1/users/`

`GET /api/v1/users/{user_id}`

`DELETE /api/v1/users/{user_id}`

`PUT /api/v1/users/{user_id}`