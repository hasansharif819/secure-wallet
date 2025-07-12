import pytest

@pytest.mark.asyncio
async def test_wallet_flow(async_client):
    # Register user
    await async_client.post("/auth/register", json={"email": "sharif@gmail.com", "password": "123456"})

    # Login using form data
    login_res = await async_client.post("/auth/login", json={
        "email": "sharif@gmail.com",
        "password": "123456"
    })

    print("LOGIN STATUS:", login_res.status_code)
    print("LOGIN RESPONSE:", login_res.text)

    assert login_res.status_code == 200, "Login failed"
    token_data = login_res.json()
    assert "access_token" in token_data, f"access_token missing. Got: {token_data}"

    token = token_data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Check balance
    res = await async_client.get("/wallet/balance", headers=headers)
    assert res.status_code == 200
    assert res.json()["balance"] == 0.0
