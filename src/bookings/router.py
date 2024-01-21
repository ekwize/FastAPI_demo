from datetime import date

from fastapi import APIRouter, Depends
from pydantic import parse_obj_as
from fastapi_versioning import version


from src.bookings.dao import BookingDAO
from src.bookings.schemas import SBooking
from src.exceptions import RoomCannotBooked
from src.tasks.tasks import send_booking_confirmation_email
from src.users.dependencies import get_current_user
from src.users.models import Users


router = APIRouter(
    prefix="/bookings",
    tags=["Бронирование"]
)

# @router.get("")
# async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBooking]:
#     return await BookingDAO.find_all(user_id=user.id)


@router.post("")
@version(1)
async def add_booking(
    room_id: int, date_from: date, date_to: date,
    user: Users = Depends(get_current_user)
):
    booking = await BookingDAO.add(user.id, room_id, date_from, date_to)
    if not booking:
        raise RoomCannotBooked
    booking_dict = parse_obj_as(SBooking, booking).model_dump()
    send_booking_confirmation_email.delay(booking_dict, user.email)
    return booking_dict








