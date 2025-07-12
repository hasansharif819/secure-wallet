import pytest

@pytest.mark.asyncio
async def test_register_and_login(async_client):
    # Register
    res = await async_client.post("/auth/register", json={"email": "test@mail.com", "password": "123456"})
    assert res.status_code == 200
    user = res.json()
    assert user["email"] == "test@mail.com"

    # Login
    res = await async_client.post("/auth/login", json={"email": "test@mail.com", "password": "123456"})
    assert res.status_code == 200
    token = res.json()["access_token"]
    assert token