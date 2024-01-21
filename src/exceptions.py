from fastapi import HTTPException, status


class BookingException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, 
                         detail=self.detail)


class UserAlreadyExists(BookingException):
    status_code=status.HTTP_409_CONFLICT 
    detail="Пользователь уже существует"


class IncorrectEmailOrPassword(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED 
    detail="Неверная почта или пароль"


class TokenExpired(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Токен истек"


class TokenAbsentException(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Токен отсутствует"

class IncorrectTokenFormatException(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Неверный формат токена"


class UserIsNotPresent(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED

class RoomCannotBooked(BookingException):
    status_code=status.HTTP_409_CONFLICT
    detail="Не осталось свободных мест"









