from fastapi import APIRouter, Response, Depends
from starlette.responses import JSONResponse

from common.authentication import oauth2_scheme, verify_jwt_token
from common.validators import is_login_valid
from users.exceptions import UserAlreadyExistsException, UserInvalidEmailException, UserNotExistException, \
    UserWrongPasswordException, UserWrongTokenSchemaException
from users.models import UserLoginData, UserRegisterData, UserUpdateData
from users.service import create_user, get_user_by_login, get_all_users, delete_user_by_login, update_user_by_login, \
    authenticate_user, verify_user_identify

router = APIRouter(prefix="/api/v1/users")


@router.get("/{user_id}",
            responses={
                200: {"description": "User's data successfully listed"},
                403: {"description": "User does not have permission to use this service"},
                404: {"description": "User with provided login does not exist"},
            },
            )
async def get_user(user_id: str, token: str = Depends(oauth2_scheme)):
    """
    Return information about specific user
    """
    try:
        users_credentials = verify_jwt_token(token=token)
        if not verify_user_identify(login=users_credentials["login"], password=users_credentials["password"]):
            return Response(status_code=403, content="User does not have permission to use this service",
                            media_type="text/plain")
        user_data = get_user_by_login(login=user_id)
        return JSONResponse(status_code=200, content=user_data, media_type="application/json")

    except UserWrongTokenSchemaException:
        return Response(status_code=403, content="User does not have permission to use this service",
                        media_type="text/plain")
    except UserNotExistException:
        return Response(status_code=404, content=f"User with login {user_id} does not exist", media_type="text/plain")


@router.get("/",
            responses={
                200: {"description": "Users data successfully listed"},
                403: {"description": "User does not have permission to use this service"},
            },
            )
async def get_users(token: str = Depends(oauth2_scheme)):
    """
    Return all users logins
    """
    try:
        users_credentials = verify_jwt_token(token=token)
    except UserWrongTokenSchemaException:
        return Response(status_code=403, content="User does not have permission to use this service",
                        media_type="text/plain")

    if not verify_user_identify(login=users_credentials["login"], password=users_credentials["password"]):
        return Response(status_code=403, content="User does not have permission to use this service",
                        media_type="text/plain")

    users_data = get_all_users()
    return JSONResponse(status_code=200, content=users_data, media_type="application/json")


@router.post("/login",
             responses={
                 200: {"description": "User successfully logged in"},
                 401: {"description": "User's provided credentials does not match"},
             },
             )
async def login_user(payload: UserLoginData):
    """
    Authenticate user and return JWT token
    """
    try:
        token = authenticate_user(login=payload.email, password=payload.password)
        headers = {'Authorization': 'Bearer ' + token}
        return Response(status_code=200, content=f"Logged in user with email: {payload.email}",
                        media_type="application/json", headers=headers)
    except UserWrongPasswordException:
        return Response(status_code=401, content="User password or login does not match",
                        media_type="text/plain")
    except UserNotExistException:
        return Response(status_code=401, content="User password or login does not match",
                        media_type="text/plain")


@router.post("/register",
             responses={
                 200: {"description": "User successfully registered"},
                 422: {"description": "User's data is invalid"},
                 409: {"description": "User with provided login already exists"},
             },
             )
async def register_user(payload: UserRegisterData, ):
    """
    Register new user and return his ID
    """
    try:
        is_login_valid(email=payload.email)
        create_user(login=payload.email, password=payload.password)
        return Response(status_code=201, content=f"Registered user with email: {payload.email}",
                        media_type="application/json")
    except UserInvalidEmailException:
        return Response(status_code=422, content="User login is not a valid email address", media_type="text/plain")
    except UserAlreadyExistsException:
        return Response(status_code=409, content="User already exists", media_type="text/plain")


@router.delete("/{user_id}",
               responses={
                   204: {"description": "User successfully deleted"},
                   403: {"description": "User does not have permission to use this service"},
                   404: {"description": "User with provided login does not exist"},
               }, )
async def delete_user(user_id: str, token: str = Depends(oauth2_scheme)):
    """
    Delete user account basing on his ID
    """
    try:
        users_credentials = verify_jwt_token(token=token)
        if not verify_user_identify(login=users_credentials["login"], password=users_credentials["password"]):
            return Response(status_code=403, content="User does not have permission to use this service",
                            media_type="text/plain")
        delete_user_by_login(login=user_id)
        return JSONResponse(status_code=204, content=f"Deleted user with login: {user_id}",
                            media_type="application/json")
    except UserWrongTokenSchemaException:
        return Response(status_code=403, content="User does not have permission to use this service",
                        media_type="text/plain")
    except UserNotExistException:
        return Response(status_code=404, content=f"User with login {user_id} does not exist", media_type="text/plain")


@router.put("/{user_id}",
            responses={
                200: {"description": "User successfully updated"},
                403: {"description": "User does not have permission to use this service"},
                404: {"description": "User with provided login does not exist"},
            }, )
async def update_user(user_id: str, payload: UserUpdateData, token: str = Depends(oauth2_scheme)):
    """
    Update user account basing on his ID
    """
    try:
        users_credentials = verify_jwt_token(token=token)
        if not verify_user_identify(login=users_credentials["login"], password=users_credentials["password"]):
            return Response(status_code=403, content="User does not have permission to use this service",
                            media_type="text/plain")
        update_user_by_login(login=user_id, new_data=payload)
        return Response(status_code=200, content=f"User with login {user_id} have been updated with {payload}",
                        media_type="application/json")
    except UserWrongTokenSchemaException:
        return Response(status_code=403, content="User does not have permission to use this service",
                        media_type="text/plain")
    except UserNotExistException:
        return Response(status_code=404, content=f"User with login {user_id} does not exist", media_type="text/plain")
