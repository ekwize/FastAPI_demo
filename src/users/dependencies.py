 
from datetime import datetime

from fastapi import Depends, HTTPException, Request, status
from jose import ExpiredSignatureError, JWTError, jwt

from src.config import settings
from src.exceptions import (IncorrectTokenFormatException,
                            TokenAbsentException, TokenExpired,
                            UserIsNotPresent)
from src.users.dao import UsersDAO


def get_token(request: Request):
    token = request.cookies.get("booking_acces_token")
    if not token:
        raise TokenAbsentException
    return token

async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token, settings.SECRET, settings.ALGORITHM
        )

    except ExpiredSignatureError:
        raise TokenExpired
    
    except JWTError:
        raise IncorrectTokenFormatException

    user_id: str = payload.get("sub")
    if not user_id:
        raise UserIsNotPresent

    user = await UsersDAO.find_by_id(int(user_id))
    if not user:
        raise UserIsNotPresent

    return user

