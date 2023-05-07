<!-- Generator: Widdershins v4.0.1 -->

<h1 id="dokumentacja-rest-api">Dokumentacja REST API v1.0.0</h1>

> Scroll down for code samples, example requests and responses. Select a language for code samples from the tabs above
> or the mobile navigation menu.

Dokumentacja REST API dla wszystkich serwisów platformy VictorTravels

# Authentication

- oAuth2 authentication.

  - Flow: password

  - Token URL = [token](token)

| Scope | Scope Description |
|-------|-------------------|

<h1 id="dokumentacja-rest-api-endpoints-for-user-operations">Endpoints for user operations</h1>

## Get User

<a id="opIdget_user_api_v1_users__user_id__get"></a>

`GET /api/v1/users/{user_id}`

Return information about specific user

<h3 id="get-user-parameters">Parameters</h3>

| Name    | In   | Type   | Required | Description |
|---------|------|--------|----------|-------------|
| user_id | path | string | true     | none        |

> Example responses

> 200 Response

```json
null
```

<h3 id="get-user-responses">Responses</h3>

| Status | Meaning                                                                    | Description                                       | Schema                                            |
|--------|----------------------------------------------------------------------------|---------------------------------------------------|---------------------------------------------------|
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)                    | User's data successfully listed                   | Inline                                            |
| 403    | [Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)             | User does not have permission to use this service | None                                              |
| 404    | [Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)             | User with provided login does not exist           | None                                              |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)   | Validation Error                                  | [HTTPValidationError](#schemahttpvalidationerror) |
| 500    | [Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1) | Unknown error occurred                            | None                                              |

<h3 id="get-user-responseschema">Response Schema</h3>

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
OAuth2PasswordBearer
</aside>

## Update User

<a id="opIdupdate_user_api_v1_users__user_id__put"></a>

`PUT /api/v1/users/{user_id}`

Update user account basing on his ID

> Body parameter

```json
{
  "email": "string",
  "password": "string"
}
```

<h3 id="update-user-parameters">Parameters</h3>

| Name    | In   | Type                                    | Required | Description |
|---------|------|-----------------------------------------|----------|-------------|
| user_id | path | string                                  | true     | none        |
| body    | body | [UserUpdateData](#schemauserupdatedata) | true     | none        |

> Example responses

> 200 Response

```json
null
```

<h3 id="update-user-responses">Responses</h3>

| Status | Meaning                                                                  | Description                         | Schema                                            |
|--------|--------------------------------------------------------------------------|-------------------------------------|---------------------------------------------------|
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)                  | Successful Response                 | Inline                                            |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3) | Validation Error                    | [HTTPValidationError](#schemahttpvalidationerror) |
| 501    | [Not Implemented](https://tools.ietf.org/html/rfc7231#section-6.6.2)     | This feature is currently disabled. | None                                              |

<h3 id="update-user-responseschema">Response Schema</h3>

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
OAuth2PasswordBearer
</aside>

## Delete User

<a id="opIddelete_user_api_v1_users__user_id__delete"></a>

`DELETE /api/v1/users/{user_id}`

Delete user account basing on his ID

<h3 id="delete-user-parameters">Parameters</h3>

| Name    | In   | Type   | Required | Description |
|---------|------|--------|----------|-------------|
| user_id | path | string | true     | none        |

> Example responses

> 200 Response

```json
null
```

<h3 id="delete-user-responses">Responses</h3>

| Status | Meaning                                                                  | Description                         | Schema                                            |
|--------|--------------------------------------------------------------------------|-------------------------------------|---------------------------------------------------|
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)                  | Successful Response                 | Inline                                            |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3) | Validation Error                    | [HTTPValidationError](#schemahttpvalidationerror) |
| 501    | [Not Implemented](https://tools.ietf.org/html/rfc7231#section-6.6.2)     | This feature is currently disabled. | None                                              |

<h3 id="delete-user-responseschema">Response Schema</h3>

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
OAuth2PasswordBearer
</aside>

## Get Users

<a id="opIdget_users_api_v1_users__get"></a>

`GET /api/v1/users/`

Return all users logins

> Example responses

> 200 Response

```json
null
```

<h3 id="get-users-responses">Responses</h3>

| Status | Meaning                                                                    | Description                                       | Schema |
|--------|----------------------------------------------------------------------------|---------------------------------------------------|--------|
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)                    | Users data successfully listed                    | Inline |
| 403    | [Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)             | User does not have permission to use this service | None   |
| 500    | [Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1) | Unknown error occurred                            | None   |

<h3 id="get-users-responseschema">Response Schema</h3>

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
OAuth2PasswordBearer
</aside>

## Login User

<a id="opIdlogin_user_api_v1_users_login_post"></a>

`POST /api/v1/users/login`

Authenticate user and return JWT token in header

> Body parameter

```json
{
  "email": "string",
  "password": "string"
}
```

<h3 id="login-user-parameters">Parameters</h3>

| Name | In   | Type                                  | Required | Description |
|------|------|---------------------------------------|----------|-------------|
| body | body | [UserLoginData](#schemauserlogindata) | true     | none        |

> Example responses

> 200 Response

```json
null
```

<h3 id="login-user-responses">Responses</h3>

| Status | Meaning                                                                    | Description                                | Schema                                            |
|--------|----------------------------------------------------------------------------|--------------------------------------------|---------------------------------------------------|
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)                    | User successfully logged in                | Inline                                            |
| 401    | [Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)            | User's provided credentials does not match | None                                              |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)   | Validation Error                           | [HTTPValidationError](#schemahttpvalidationerror) |
| 500    | [Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1) | Unknown error occurred                     | None                                              |

<h3 id="login-user-responseschema">Response Schema</h3>

<aside class="success">
This operation does not require authentication
</aside>

## Register User

<a id="opIdregister_user_api_v1_users_register_post"></a>

`POST /api/v1/users/register`

Register new user and return his ID

> Body parameter

```json
{
  "email": "string",
  "password": "string"
}
```

<h3 id="register-user-parameters">Parameters</h3>

| Name | In   | Type                                        | Required | Description |
|------|------|---------------------------------------------|----------|-------------|
| body | body | [UserRegisterData](#schemauserregisterdata) | true     | none        |

> Example responses

> 200 Response

```json
null
```

<h3 id="register-user-responses">Responses</h3>

| Status | Meaning                                                                    | Description                             | Schema |
|--------|----------------------------------------------------------------------------|-----------------------------------------|--------|
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)                    | Successful Response                     | Inline |
| 201    | [Created](https://tools.ietf.org/html/rfc7231#section-6.3.2)               | User successfully registered            | None   |
| 409    | [Conflict](https://tools.ietf.org/html/rfc7231#section-6.5.8)              | User with provided login already exists | None   |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)   | User's login is in invalid format       | None   |
| 500    | [Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1) | Unknown error occurred                  | None   |

<h3 id="register-user-responseschema">Response Schema</h3>

<aside class="success">
This operation does not require authentication
</aside>

<h1 id="dokumentacja-rest-api-endpoints-for-payment-ms-operations">Endpoints for payment ms operations</h1>

## Buy Trip

<a id="opIdbuy_trip_api_v1_payments__reservation_id__post"></a>

`POST /api/v1/payments/{reservation_id}`

Make a payment for a specific trip reservation

<h3 id="buy-trip-parameters">Parameters</h3>

| Name           | In   | Type   | Required | Description |
|----------------|------|--------|----------|-------------|
| reservation_id | path | string | true     | none        |

> Example responses

> 200 Response

```json
null
```

<h3 id="buy-trip-responses">Responses</h3>

| Status | Meaning                                                                    | Description                                            | Schema                                            |
|--------|----------------------------------------------------------------------------|--------------------------------------------------------|---------------------------------------------------|
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)                    | Payment performed successfully                         | Inline                                            |
| 400    | [Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)           | Reservation with provided ID has already been paid for | None                                              |
| 402    | [Payment Required](https://tools.ietf.org/html/rfc7231#section-6.5.2)      | Payment for reservation have failed                    | None                                              |
| 403    | [Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)             | User does not have permission to use this service      | None                                              |
| 404    | [Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)             | Reservation with provided ID does not exist            | None                                              |
| 410    | [Gone](https://tools.ietf.org/html/rfc7231#section-6.5.9)                  | Reservation with ID has expired                        | None                                              |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)   | Validation Error                                       | [HTTPValidationError](#schemahttpvalidationerror) |
| 500    | [Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1) | Unknown error occurred                                 | None                                              |
| 503    | [Service Unavailable](https://tools.ietf.org/html/rfc7231#section-6.6.4)   | Failed to connect to backend service                   | None                                              |

<h3 id="buy-trip-responseschema">Response Schema</h3>

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
OAuth2PasswordBearer
</aside>

<h1 id="dokumentacja-rest-api-endpoints-for-purchase-ms-operations">Endpoints for purchase ms operations</h1>

## Purchase Trip

<a id="opIdpurchase_trip_api_v1_purchases__reservation_id__post"></a>

`POST /api/v1/purchases/{reservation_id}`

Make a purchase of a specific trip reservation

<h3 id="purchase-trip-parameters">Parameters</h3>

| Name           | In   | Type   | Required | Description |
|----------------|------|--------|----------|-------------|
| reservation_id | path | string | true     | none        |

> Example responses

> 200 Response

```json
null
```

<h3 id="purchase-trip-responses">Responses</h3>

| Status | Meaning                                                                    | Description                                       | Schema                                            |
|--------|----------------------------------------------------------------------------|---------------------------------------------------|---------------------------------------------------|
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)                    | Purchase was already performed                    | Inline                                            |
| 201    | [Created](https://tools.ietf.org/html/rfc7231#section-6.3.2)               | Purchase successfully created                     | None                                              |
| 403    | [Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)             | User does not have permission to use this service | None                                              |
| 404    | [Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)             | Reservation with provided ID does not exist       | None                                              |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)   | Validation Error                                  | [HTTPValidationError](#schemahttpvalidationerror) |
| 500    | [Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1) | Unknown error occurred                            | None                                              |
| 503    | [Service Unavailable](https://tools.ietf.org/html/rfc7231#section-6.6.4)   | Failed to connect to backend service              | None                                              |

<h3 id="purchase-trip-responseschema">Response Schema</h3>

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
OAuth2PasswordBearer
</aside>

<h1 id="dokumentacja-rest-api-endpoints-for-reservations-ms-operations">Endpoints for reservations ms operations</h1>

## Make Reservation

<a id="opIdmake_reservation_api_v1_reservations__trip_offer_id__post"></a>

`POST /api/v1/reservations/{trip_offer_id}`

Make a reservation of a specific trip

> Body parameter

```json
{
  "hotel_id": "string",
  "room_type": "string",
  "connection_id_to": "string",
  "connection_id_from": "string",
  "head_count": 0,
  "price": 0
}
```

<h3 id="make-reservation-parameters">Parameters</h3>

| Name          | In   | Type                                              | Required | Description |
|---------------|------|---------------------------------------------------|----------|-------------|
| trip_offer_id | path | string                                            | true     | none        |
| body          | body | [TripReservationData](#schematripreservationdata) | true     | none        |

> Example responses

> 200 Response

```json
null
```

<h3 id="make-reservation-responses">Responses</h3>

| Status | Meaning                                                                    | Description                                            | Schema                                            |
|--------|----------------------------------------------------------------------------|--------------------------------------------------------|---------------------------------------------------|
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)                    | Successful Response                                    | Inline                                            |
| 201    | [Created](https://tools.ietf.org/html/rfc7231#section-6.3.2)               | Reservation successfully created                       | None                                              |
| 400    | [Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)           | Trip with provided ID does not have enough places left | None                                              |
| 403    | [Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)             | User does not have permission to use this service      | None                                              |
| 404    | [Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)             | Trip with provided ID does not exist                   | None                                              |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)   | Validation Error                                       | [HTTPValidationError](#schemahttpvalidationerror) |
| 500    | [Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1) | Unknown error occurred                                 | None                                              |
| 503    | [Service Unavailable](https://tools.ietf.org/html/rfc7231#section-6.6.4)   | Failed to connect to backend service                   | None                                              |

<h3 id="make-reservation-responseschema">Response Schema</h3>

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
OAuth2PasswordBearer
</aside>

<h1 id="dokumentacja-rest-api-endpoints-for-trip-researcher-operations">Endpoints for trip researcher operations</h1>

## Get Trip

<a id="opIdget_trip_api_v1_trips__trip_id__get"></a>

`GET /api/v1/trips/{trip_id}`

Return information about specific trip

<h3 id="get-trip-parameters">Parameters</h3>

| Name    | In   | Type   | Required | Description |
|---------|------|--------|----------|-------------|
| trip_id | path | string | true     | none        |

> Example responses

> 200 Response

```json
null
```

<h3 id="get-trip-responses">Responses</h3>

| Status | Meaning                                                                    | Description                          | Schema                                            |
|--------|----------------------------------------------------------------------------|--------------------------------------|---------------------------------------------------|
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)                    | Trip's data successfully listed      | Inline                                            |
| 404    | [Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)             | Trip with provided ID does not exist | None                                              |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)   | Validation Error                     | [HTTPValidationError](#schemahttpvalidationerror) |
| 500    | [Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1) | Unknown error occurred               | None                                              |
| 503    | [Service Unavailable](https://tools.ietf.org/html/rfc7231#section-6.6.4)   | Failed to connect to backend service | None                                              |

<h3 id="get-trip-responseschema">Response Schema</h3>

<aside class="success">
This operation does not require authentication
</aside>

## Get Trips

<a id="opIdget_trips_api_v1_trips__get"></a>

`GET /api/v1/trips/`

Return information about trips meeting given query

<h3 id="get-trips-parameters">Parameters</h3>

| Name             | In    | Type          | Required | Description |
|------------------|-------|---------------|----------|-------------|
| adults           | query | integer       | false    | none        |
| kids_to_3yo      | query | integer       | false    | none        |
| kids_to_10yo     | query | integer       | false    | none        |
| kids_to_18yo     | query | integer       | false    | none        |
| date_from        | query | string(date)  | false    | none        |
| date_to          | query | string(date)  | false    | none        |
| departure_region | query | array[string] | false    | none        |
| arrival_region   | query | array[string] | false    | none        |
| transport        | query | array[string] | false    | none        |
| order            | query | string        | false    | none        |
| diet             | query | array[string] | false    | none        |
| max_price        | query | integer       | false    | none        |

> Example responses

> 200 Response

```json
null
```

<h3 id="get-trips-responses">Responses</h3>

| Status | Meaning                                                                    | Description                              | Schema                                            |
|--------|----------------------------------------------------------------------------|------------------------------------------|---------------------------------------------------|
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)                    | Trips fetched successfully               | Inline                                            |
| 400    | [Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)           | Invalid tour researcher query parameters | None                                              |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)   | Validation Error                         | [HTTPValidationError](#schemahttpvalidationerror) |
| 500    | [Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1) | Unknown error occurred                   | None                                              |
| 503    | [Service Unavailable](https://tools.ietf.org/html/rfc7231#section-6.6.4)   | Failed to connect to backend service     | None                                              |

<h3 id="get-trips-responseschema">Response Schema</h3>

<aside class="success">
This operation does not require authentication
</aside>

# Schemas

<h2 id="tocS_HTTPValidationError">HTTPValidationError</h2>
<!-- backwards compatibility -->
<a id="schemahttpvalidationerror"></a>
<a id="schema_HTTPValidationError"></a>
<a id="tocShttpvalidationerror"></a>
<a id="tocshttpvalidationerror"></a>

```json
{
  "detail": [
    {
      "loc": [
        "string"
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}

```

HTTPValidationError

### Properties

| Name   | Type                                        | Required | Restrictions | Description |
|--------|---------------------------------------------|----------|--------------|-------------|
| detail | [[ValidationError](#schemavalidationerror)] | false    | none         | none        |

<h2 id="tocS_TripReservationData">TripReservationData</h2>
<!-- backwards compatibility -->
<a id="schematripreservationdata"></a>
<a id="schema_TripReservationData"></a>
<a id="tocStripreservationdata"></a>
<a id="tocstripreservationdata"></a>

```json
{
  "hotel_id": "string",
  "room_type": "string",
  "connection_id_to": "string",
  "connection_id_from": "string",
  "head_count": 0,
  "price": 0
}

```

TripReservationData

### Properties

| Name               | Type    | Required | Restrictions | Description |
|--------------------|---------|----------|--------------|-------------|
| hotel_id           | string  | true     | none         | none        |
| room_type          | string  | true     | none         | none        |
| connection_id_to   | string  | true     | none         | none        |
| connection_id_from | string  | true     | none         | none        |
| head_count         | integer | true     | none         | none        |
| price              | number  | true     | none         | none        |

<h2 id="tocS_UserLoginData">UserLoginData</h2>
<!-- backwards compatibility -->
<a id="schemauserlogindata"></a>
<a id="schema_UserLoginData"></a>
<a id="tocSuserlogindata"></a>
<a id="tocsuserlogindata"></a>

```json
{
  "email": "string",
  "password": "string"
}

```

UserLoginData

### Properties

| Name     | Type   | Required | Restrictions | Description |
|----------|--------|----------|--------------|-------------|
| email    | string | true     | none         | none        |
| password | string | true     | none         | none        |

<h2 id="tocS_UserRegisterData">UserRegisterData</h2>
<!-- backwards compatibility -->
<a id="schemauserregisterdata"></a>
<a id="schema_UserRegisterData"></a>
<a id="tocSuserregisterdata"></a>
<a id="tocsuserregisterdata"></a>

```json
{
  "email": "string",
  "password": "string"
}

```

UserRegisterData

### Properties

| Name     | Type   | Required | Restrictions | Description |
|----------|--------|----------|--------------|-------------|
| email    | string | true     | none         | none        |
| password | string | true     | none         | none        |

<h2 id="tocS_UserUpdateData">UserUpdateData</h2>
<!-- backwards compatibility -->
<a id="schemauserupdatedata"></a>
<a id="schema_UserUpdateData"></a>
<a id="tocSuserupdatedata"></a>
<a id="tocsuserupdatedata"></a>

```json
{
  "email": "string",
  "password": "string"
}

```

UserUpdateData

### Properties

| Name     | Type   | Required | Restrictions | Description |
|----------|--------|----------|--------------|-------------|
| email    | string | true     | none         | none        |
| password | string | true     | none         | none        |

<h2 id="tocS_ValidationError">ValidationError</h2>
<!-- backwards compatibility -->
<a id="schemavalidationerror"></a>
<a id="schema_ValidationError"></a>
<a id="tocSvalidationerror"></a>
<a id="tocsvalidationerror"></a>

```json
{
  "loc": [
    "string"
  ],
  "msg": "string",
  "type": "string"
}

```

ValidationError

### Properties

| Name | Type    | Required | Restrictions | Description |
|------|---------|----------|--------------|-------------|
| loc  | [anyOf] | true     | none         | none        |

anyOf

| Name          | Type   | Required | Restrictions | Description |
|---------------|--------|----------|--------------|-------------|
| » *anonymous* | string | false    | none         | none        |

or

| Name          | Type    | Required | Restrictions | Description |
|---------------|---------|----------|--------------|-------------|
| » *anonymous* | integer | false    | none         | none        |

continued

| Name | Type   | Required | Restrictions | Description |
|------|--------|----------|--------------|-------------|
| msg  | string | true     | none         | none        |
| type | string | true     | none         | none        |

