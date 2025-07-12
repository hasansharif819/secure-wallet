import pytest_asyncio
from httpx import AsyncClient
from httpx import ASGITransport
from app.main import app
from app.database.db import Base, engine


@pytest_asyncio.fixture(scope="session")
async def prepare_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest_asyncio.fixture
async def async_client(prepare_database):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
