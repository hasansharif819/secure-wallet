import pytest

@pytest.mark.asyncio
async def test_withdraw_flow(async_client):
    # Register the user
    await async_client.post("/auth/register", json={"name": "withdraw", "email": "withdraw@test.com", "password": "123456"})

    # Login with form data (not JSON)
    login_res = await async_client.post("/auth/login", data={
        "username": "withdraw@test.com",
        "password": "123456"
    })

    # Print for debugging if needed
    print("LOGIN STATUS:", login_res.status_code)
    print("LOGIN RESPONSE:", login_res.text)

    assert login_res.status_code == 200, "Login failed"
    token_data = login_res.json()
    assert "access_token" in token_data, f"access_token missing. Got: {token_data}"

    token = token_data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Top-up
    res = await async_client.post("/wallet/top-up", headers=headers, json={"amount": 200.0})
    assert res.status_code == 200

    # Withdraw (valid)
    res = await async_client.post("/wallet/withdraw", headers=headers, json={"amount": 150.0})
    assert res.status_code == 200
    assert res.json()["amount"] == -150.0

    # Withdraw (insufficient balance)
    res = await async_client.post("/wallet/withdraw", headers=headers, json={"amount": 100.0})
    assert res.status_code == 400
    assert "Insufficient balance" in res.text
