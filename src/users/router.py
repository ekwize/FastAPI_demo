from fastapi import APIRouter, Depends, Response

from src.exceptions import IncorrectEmailOrPassword, UserAlreadyExists
from src.users.auth import auth_user, create_access_token, get_password_hash
from src.users.dao import UsersDAO
from src.users.dependencies import get_current_user
from src.users.models import Users
from src.users.schemas import SUserAuth

router = APIRouter(
    prefix="/auth",
    tags=["Auth & Пользователи"]
)


@router.post("/register")
async def register_user(user_data: SUserAuth):
    existing_user = await UsersDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExists
    hashed_password = get_password_hash(user_data.password)
    await UsersDAO.add(email=user_data.email, hashed_password=hashed_password)


@router.post("/login")
async def login_user(response: Response, user_data: SUserAuth):
    user = await auth_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectEmailOrPassword
    acces_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("booking_acces_token", acces_token, httponly=True)
    return acces_token


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("booking_acces_token")


@router.get("/me")
async def read_users_me(current_user: Users = Depends(get_current_user)):
    return current_user



