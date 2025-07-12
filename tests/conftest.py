import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.main import app
from app.database.db import get_db, Base, engine

@pytest.fixture(scope="session")
async def prepare_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

@pytest.fixture()
async def async_client(prepare_database):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac