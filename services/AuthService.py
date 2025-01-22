from fastapi import Header, HTTPException
import os
import requests


class AuthService:
    """Service class to handle authentication and user data operations."""

    @staticmethod
    def authenticate_user(auth_header):
        """
        Authenticate the user and return user_id based on the authorization header.
        Raises exceptions for invalid authorization or missing user ID.
        """
        if not auth_header:
            raise Exception("Authorization header is required")
        auth_url = os.getenv('AUTH_URL')
        response = requests.get(f"{auth_url}/user_id/token", headers={"Authorization": auth_header})
        if response.status_code != 200:
            raise Exception("Invalid authorization")
        user_id = response.json().get('userId')
        if not user_id:
            raise Exception("User ID not found in token response")
        return user_id



async def authenticate_user(authorization: str = Header(None)):
    """
    Dependency to authenticate the request using the Authorization header.

    :param authorization: The Authorization header containing the bearer token.
    :return: The user_id retrieved from the authentication service.
    """
    try:
        return AuthService.authenticate_user(auth_header=authorization)
    except Exception as auth_error:
        raise HTTPException(status_code=401, detail=str(auth_error))

