import pytest

@pytest.mark.asyncio
async def test_wallet_flow(async_client):
    await async_client.post("/auth/register", json={"email": "wallet@test.com", "password": "123456"})
    login_res = await async_client.post("/auth/login", json={"email": "wallet@test.com", "password": "123456"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Get balance (should be 0.0)
    res = await async_client.get("/wallet/balance", headers=headers)
    assert res.status_code == 200
    assert res.json()["balance"] == 0.0

    # Top-up
    res = await async_client.post("/wallet/top-up", headers=headers, json={"amount": 100.0})
    assert res.status_code == 200
    assert res.json()["amount"] == 100.0

    # Check new balance
    res = await async_client.get("/wallet/balance", headers=headers)
    assert res.json()["balance"] == 100.0

    # Get transactions
    res = await async_client.get("/wallet/transactions", headers=headers)
    txs = res.json()
    assert len(txs) == 1
    assert txs[0]["amount"] == 100.0