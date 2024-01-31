import asyncio
from typing import AsyncGenerator
from httpx import AsyncClient

import pytest
from fastapi.testclient import TestClient
# from httpx import AsyncClient

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from src.menu.models import menu_table
from src.submenu.models import submenu_table
from src.dish.models import dish_table


from src.database import get_async_session
from src.database import metadata
from src.config import (DBT_HOST, DBT_NAME, DBT_PASS, DBT_PORT, DBT_USER)
from src.main import app
from sqlalchemy import insert, select

# DATABASE
DATABASE_URL_TEST = f"postgresql+asyncpg://{DBT_USER}:{DBT_PASS}@{DBT_HOST}:{DBT_PORT}/{DBT_NAME}"

engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
async_session_maker = sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)
metadata.bind = engine_test

async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

app.dependency_overrides[get_async_session] = override_get_async_session

@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.create_all)
    yield
    async with engine_test.begin() as conn:#########################################################
        await conn.run_sync(metadata.drop_all)####################################################

# SETUP
@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

client = TestClient(app)

@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test", follow_redirects=True) as ac:
        yield ac


# Фикстура для сохранения данных о добавленном меню
@pytest.fixture(scope="module")
async def added_menu_data(ac: AsyncClient):
    async with async_session_maker() as session:
        query = select(menu_table)
        result = await session.execute(query)
        res = result.all()
        menu_data = []
        menu_data.append(res[0][0])
    return menu_data


# Фикстура для сохранения данных о добавленном меню
@pytest.fixture(scope="module")
async def added_submenu_data(ac: AsyncClient):
    async with async_session_maker() as session:
        query = select(submenu_table)
        result = await session.execute(query)
        res = result.all()
        submenu_data = []
        submenu_data.append(res[0][0])
        submenu_data.append(res[0][3])
    return submenu_data


# Фикстура для сохранения данных о добавленном меню
@pytest.fixture(scope="module")
async def added_dish_data(ac: AsyncClient):
    async with async_session_maker() as session:
        query = select(dish_table)
        result = await session.execute(query)
        res = result.all()
        dish_data = []
        dish_data.append(res[0][0])
        dish_data.append(res[0][4])
    return dish_data


