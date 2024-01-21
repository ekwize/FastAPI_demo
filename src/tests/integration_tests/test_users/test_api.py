import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("email, password, status_code", [
    ("alina@gmail.com", "AlinaPRO", 200),
    ("alina@gmail.com", "AlinaPRO1", 409)
])
async def test_register_user(ac: AsyncClient, email, password, status_code):
    response = await ac.post("/auth/register", json={
                  "email" : email,
                  "password" : password,
    })
    
    assert response.status_code == status_code

@pytest.mark.parametrize("email, password, status_code", [
    ("test@test.com", "test", 200)
])
async def test_login_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post("/auth/login", json={
        "email": email,
        "password": password
    })

    assert response.status_code == status_code