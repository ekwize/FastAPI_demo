import asyncio
import datetime
import json

import pytest
from httpx import AsyncClient
from sqlalchemy import insert

from src.bookings.models import Bookings
from src.config import settings
from src.database import Base, async_session, engine
from src.hotels.models import Hotels, Rooms
from src.main import app as fastapi_app
from src.users.models import Users


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


    def open_mock_json(model: str):
        with open(f"src/tests/mock_{model}.json", encoding="utf-8") as file:
            return json.load(file)

    hotels = open_mock_json("hotels")
    rooms = open_mock_json("rooms")
    users = open_mock_json("users")
    bookings = open_mock_json("bookings")

    for booking in bookings:
        booking["date_from"] = datetime.datetime.strptime(booking["date_to"], "%Y-%m-%d")
        booking["date_to"] = datetime.datetime.strptime(booking["date_to"],"%Y-%m-%d")


    async with async_session() as session:
        add_hotels = insert(Hotels).values(hotels)
        add_rooms = insert(Rooms).values(rooms)
        add_users = insert(Users).values(users)
        add_bookings = insert(Bookings).values(bookings)

        await session.execute(add_hotels)
        await session.execute(add_rooms)
        await session.execute(add_users)
        await session.execute(add_bookings)

        await session.commit()


@pytest.mark.asyncio(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def ac():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        yield ac

@pytest.fixture(scope="session")
async def authenticated_ac():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        await ac.post("/auth/login", json={
                "email" : "test@test.com",
                "password" : "test",
        })
    
        assert ac.cookies["booking_acces_token"]
        yield ac        
        







