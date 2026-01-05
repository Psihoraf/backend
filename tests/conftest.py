import json

import pytest
from httpx import AsyncClient, ASGITransport

from src.Schemas.hotels import HotelAdd
from src.Schemas.rooms import RoomsAdd
from src.config import settings
from src.database import Base, engine_null_pool, async_session_maker_null_pool
from src.main import app
from src.models import *
from src.utils.db_manager import DBManager


@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"

@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    with open('tests/mock_hotels.json', 'r', encoding='utf-8') as hotels_json:
        hotels_data = json.load(hotels_json)
    with open('tests/mock_rooms.json', 'r', encoding='utf-8') as room_json:
        rooms_data = json.load(room_json)

    hotels = [HotelAdd.model_validate(hotel) for hotel in hotels_data]
    rooms = [RoomsAdd.model_validate(room) for room in rooms_data]

    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        await db.hotels.add_bulk(hotels)
        await db.rooms.add_bulk(rooms)
        await db.commit()

@pytest.fixture(scope="session", autouse=True)
async def register_user(setup_database):
    async with  AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        await ac.post(
            "/auth/register",
            json={
                "email": "kot@pes.com",
                "password": "1234"
            }
        )