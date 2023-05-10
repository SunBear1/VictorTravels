import logging

from fastapi import APIRouter, Response, Depends
from starlette import status
from starlette.responses import JSONResponse

from common.authentication import oauth2_scheme, verify_jwt_token
from common.validators import is_login_valid
from users.exceptions import UserAlreadyExistsException, UserInvalidEmailException, UserNotExistException, \
    UserWrongPasswordException, UserWrongTokenSchemaException
from users.models import UserLoginData, UserRegisterData, UserUpdateData
from users.service import create_user, get_user_by_login, get_all_users, authenticate_user, verify_user_identify

router = APIRouter(prefix="/api/v1/users")

logger = logging.getLogger("gateway")


@router.get("/{user_id}",
            responses={
                200: {"description": "User's data successfully listed"},
                403: {"description": "User does not have permission to use this service"},
                404: {"description": "User with provided login does not exist"},
                500: {"description": "Unknown error occurred"},
            },
            )
async def get_user(user_id: str, token: str = Depends(oauth2_scheme)):
    """
    Return information about specific user
    """
    try:
        users_credentials = verify_jwt_token(token=token)
        if not verify_user_identify(login=users_credentials["login"], password=users_credentials["password"]):
            return Response(status_code=status.HTTP_403_FORBIDDEN,
                            content="User does not have permission to use this service",
                            media_type="text/plain")
        user_data = get_user_by_login(login=user_id)
        return JSONResponse(status_code=status.HTTP_200_OK, content=user_data, media_type="application/json")
    except UserWrongTokenSchemaException:
        return Response(status_code=status.HTTP_403_FORBIDDEN,
                        content="User does not have permission to use this service",
                        media_type="text/plain")
    except UserNotExistException:
        return Response(status_code=status.HTTP_404_NOT_FOUND, content=f"User with login {user_id} does not exist",
                        media_type="text/plain")
    except Exception as ex:
        logger.info(f"Exception in gateway occurred: {ex}")
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/",
            responses={
                200: {"description": "Users data successfully listed"},
                403: {"description": "User does not have permission to use this service"},
                500: {"description": "Unknown error occurred"},
            },
            )
async def get_users(token: str = Depends(oauth2_scheme)):
    """
    Return all users logins
    """
    try:
        users_credentials = verify_jwt_token(token=token)
        if not verify_user_identify(login=users_credentials["login"], password=users_credentials["password"]):
            return Response(status_code=status.HTTP_403_FORBIDDEN,
                            content="User does not have permission to use this service",
                            media_type="text/plain")

        users_data = get_all_users()
        return JSONResponse(status_code=status.HTTP_200_OK, content=users_data, media_type="application/json")
    except UserWrongTokenSchemaException:
        return Response(status_code=status.HTTP_403_FORBIDDEN,
                        content="User does not have permission to use this service",
                        media_type="text/plain")
    except Exception as ex:
        logger.info(f"Exception in gateway occurred: {ex}")
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post("/login",
             responses={
                 200: {"description": "User successfully logged in"},
                 401: {"description": "User's provided credentials does not match"},
                 500: {"description": "Unknown error occurred"},
             },
             )
async def login_user(payload: UserLoginData):
    """
    Authenticate user and return JWT token in header
    """
    try:
        token = authenticate_user(login=payload.email, password=payload.password)
        headers = {'Authorization': 'Bearer ' + token}
        logger.info(f"User {payload.email} successfully logged in.")
        return Response(status_code=status.HTTP_200_OK, content=f"Logged in user with email: {payload.email}",
                        media_type="application/json", headers=headers)
    except UserWrongPasswordException:
        logger.info(f"User {payload.email} password or login does not match.")
        return Response(status_code=status.HTTP_401_UNAUTHORIZED, content="User password or login does not match",
                        media_type="text/plain")
    except UserNotExistException:
        logger.info(f"User {payload.email} does not exist.")
        return Response(status_code=status.HTTP_401_UNAUTHORIZED, content="User password or login does not match",
                        media_type="text/plain")
    except Exception as ex:
        logger.info(f"Exception in gateway occurred: {ex}")
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post("/register",
             responses={
                 201: {"description": "User successfully registered"},
                 409: {"description": "User with provided login already exists"},
                 422: {"description": "User's login is in invalid format"},
                 500: {"description": "Unknown error occurred"},
             },
             )
async def register_user(payload: UserRegisterData):
    """
    Register new user and return his ID
    """
    try:
        is_login_valid(email=payload.email)
        create_user(login=payload.email, password=payload.password)
        logger.info(f"User {payload.email} successfully registered.")
        return Response(status_code=status.HTTP_201_CREATED, content=f"Registered user with email: {payload.email}",
                        media_type="application/json")
    except UserInvalidEmailException:
        logger.info(f"User's login {payload.email} is in invalid format.")
        return Response(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content="User login is not a valid email "
                                                                                  "address", media_type="text/plain")
    except UserAlreadyExistsException:
        logger.info(f"User with login {payload.email} already exists.")
        return Response(status_code=status.HTTP_409_CONFLICT, content="User already exists", media_type="text/plain")
    except Exception as ex:
        logger.info(f"Exception in gateway occurred: {ex}")
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete("/{user_id}",
               responses={
                   # 204: {"description": "User successfully deleted"},
                   # 403: {"description": "User does not have permission to use this service"},
                   # 404: {"description": "User with provided login does not exist"},
                   501: {"description": "This feature is currently disabled."}
               }, )
async def delete_user(user_id: str, token: str = Depends(oauth2_scheme)):
    """
    Delete user account basing on his ID
    """
    return Response(status_code=status.HTTP_501_NOT_IMPLEMENTED, media_type="text/plain")
    # try:
    #     users_credentials = verify_jwt_token(token=token)
    #     if not verify_user_identify(login=users_credentials["login"], password=users_credentials["password"]):
    #         return Response(status_code=403, content="User does not have permission to use this service",
    #                         media_type="text/plain")
    #     delete_user_by_login(login=user_id)
    #     return JSONResponse(status_code=204, content=f"Deleted user with login: {user_id}",
    #                         media_type="application/json")
    # except UserWrongTokenSchemaException:
    #     return Response(status_code=403, content="User does not have permission to use this service",
    #                     media_type="text/plain")
    # except UserNotExistException:
    #     return Response(status_code=404, content=f"User with login {user_id} does not exist", media_type="text/plain")


@router.put("/{user_id}",
            responses={
                # 200: {"description": "User successfully updated"},
                # 403: {"description": "User does not have permission to use this service"},
                # 404: {"description": "User with provided login does not exist"},
                501: {"description": "This feature is currently disabled."}
            }, )
async def update_user(user_id: str, payload: UserUpdateData, token: str = Depends(oauth2_scheme)):
    """
    Update user account basing on his ID
    """
    return Response(status_code=status.HTTP_501_NOT_IMPLEMENTED, media_type="text/plain")
    # try:
    #     users_credentials = verify_jwt_token(token=token)
    #     if not verify_user_identify(login=users_credentials["login"], password=users_credentials["password"]):
    #         return Response(status_code=403, content="User does not have permission to use this service",
    #                         media_type="text/plain")
    #     update_user_by_login(login=user_id, new_data=payload)
    #     return Response(status_code=200, content=f"User with login {user_id} have been updated with {payload}",
    #                     media_type="application/json")
    # except UserWrongTokenSchemaException:
    #     return Response(status_code=403, content="User does not have permission to use this service",
    #                     media_type="text/plain")
    # except UserNotExistException:
    #     return Response(status_code=404, content=f"User with login {user_id} does not exist", media_type="text/plain")
