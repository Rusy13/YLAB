from asyncio import sleep
import pytest
from sqlalchemy import insert, select
from conftest import ac, client, async_session_maker
from src.submenu.models import submenu_table
from src.menu.models import menu_table
from src.dish.models import dish_table

from conftest import async_session_maker
from http import HTTPStatus
from typing import Any
from httpx import AsyncClient










async def test_post_menu1(ac: AsyncClient):
    """Добавление нового меню."""
    response = await ac.post("/api/v1/menus", json={
    "title": "My menu 1",
    "description": "My menu description 1"
})
    assert response.status_code == HTTPStatus.CREATED, \
        'Статус ответа не 201'
    assert 'id' in response.json(), 'Идентификатора меню нет в ответе'
    assert 'title' in response.json(), 'Названия меню нет в ответе'
    assert 'description' in response.json(), 'Описания меню нет в ответе'
    assert 'submenus_count' in response.json(), \
        'Количества подменю нет в ответе'
    assert 'dishes_count' in response.json(), 'Количества блюд нет в ответе'
    assert response.json()['title'] == "My menu 1", \
        'Название меню не соответствует ожидаемому'
    assert response.json()['description'] == "My menu description 1", \
        'Описание меню не соответствует ожидаемому'






async def test_post_submenu1(ac: AsyncClient):
    async with async_session_maker() as session:
        query = select(menu_table)
        result = await session.execute(query)
        res = result.all()
    """Добавление нового меню."""
    response = await ac.post(f"/api/v1/menus/{res[0][0]}/submenus", json={
    "title": "My submenu 1",
    "description": "My submenu description 1"
})
    assert response.status_code == HTTPStatus.CREATED, \
        'Статус ответа не 201'
    assert 'id' in response.json(), 'Идентификатора меню нет в ответе'
    assert 'title' in response.json(), 'Названия меню нет в ответе'
    assert 'description' in response.json(), 'Описания меню нет в ответе'
    assert 'dishes_count' in response.json(), 'Количества блюд нет в ответе'
    assert response.json()['title'] == "My submenu 1", \
        'Название меню не соответствует ожидаемому'
    assert response.json()['description'] == "My submenu description 1", \
        'Описание меню не соответствует ожидаемому'











async def test_post_dish1(ac: AsyncClient):
    async with async_session_maker() as session:
        query = select(submenu_table)
        result = await session.execute(query)
        res = result.all()
        print(res)
        sm1 = str(res[0][0])
        m1 = str(res[0][3])
    """Добавление нового блюда."""
    response = await ac.post(f"/api/v1/menus/{m1}/submenus/{sm1}/dishes", json={
    "title": "My dish 2",
    "description": "My dish description 2",
    "price": "13.50"
})
    assert response.status_code == HTTPStatus.CREATED, \
        'Статус ответа не 201'
    assert 'id' in response.json(), 'Идентификатора меню нет в ответе'
    assert 'title' in response.json(), 'Названия меню нет в ответе'
    assert 'description' in response.json(), 'Описания меню нет в ответе'
    # assert 'dishes_count' in response.json(), 'Количества блюд нет в ответе'
    assert response.json()['title'] == "My dish 2", \
        'Название меню не соответствует ожидаемому'
    assert response.json()['description'] == "My dish description 2", \
        'Описание меню не соответствует ожидаемому'
    assert response.json()['price'] == "13.5", \
        'Описание цены не соответствует ожидаемому'
    





async def test_post_dish2(ac: AsyncClient):
    async with async_session_maker() as session:
        query = select(submenu_table)
        result = await session.execute(query)
        res = result.all()
        print(res)
        sm1 = str(res[0][0])
        m1 = str(res[0][3])
    """Добавление нового блюда."""
    response = await ac.post(f"/api/v1/menus/{m1}/submenus/{sm1}/dishes", json={
    "title": "My dish 1",
    "description": "My dish description 1",
    "price": "12.50"
})
    assert response.status_code == HTTPStatus.CREATED, \
        'Статус ответа не 201'
    assert 'id' in response.json(), 'Идентификатора меню нет в ответе'
    assert 'title' in response.json(), 'Названия меню нет в ответе'
    assert 'description' in response.json(), 'Описания меню нет в ответе'
    # assert 'dishes_count' in response.json(), 'Количества блюд нет в ответе'
    assert response.json()['title'] == "My dish 1", \
        'Название меню не соответствует ожидаемому'
    assert response.json()['description'] == "My dish description 1", \
        'Описание меню не соответствует ожидаемому'
    assert response.json()['price'] == "12.5", \
        'Описание цены не соответствует ожидаемому'









async def test_get_patched_menu1(ac: AsyncClient):
    async with async_session_maker() as session:
        query = select(menu_table)
        result = await session.execute(query)
        res = result.all()
    """Получение обновленного меню."""
    query = select(menu_table)
    response = await ac.get(f"/api/v1/menus/{res[0][0]}")
    query = select(menu_table)
    assert response.status_code == HTTPStatus.OK, 'Статус ответа не 200'
    assert response.json()['submenus_count'] == 1, \
        'Количество подменю не соответствует ожидаемому'
    assert response.json()['dishes_count'] == 2, \
        'Количество блюд не соответствует ожидаемому'









async def test_get_submenu_count1(ac: AsyncClient):
    async with async_session_maker() as session:
        query = select(submenu_table)
        result = await session.execute(query)
        res = result.all()
        print(res[0][0])

    async with async_session_maker() as session:
        query = select(submenu_table)
        result = await session.execute(query)
        res1 = result.all()
        print(res1[0][3])

    """Изменение текущего меню."""
    response = await ac.get(f"/api/v1/menus/{res1[0][3]}/submenus/{res[0][0]}")

    assert response.json()['dishes_count'] == 2, \
        'Количество блюд не соответствует ожидаемому'









async def test_delete_dish(ac: AsyncClient, added_dish_data, added_submenu_data):
    dish_id = str(added_dish_data[0])
    submenu_id = str(added_dish_data[1])
    menu_id = str(added_submenu_data[1])
    print(dish_id)
    print(submenu_id)
    print(menu_id)
    async with async_session_maker() as session:
        query = select(menu_table)
        result = await session.execute(query)
        res = result.all()
        print(res)
    """Удаление текущего меню."""
    response = await ac.delete(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
    assert response.status_code == HTTPStatus.OK, \
        'Статус ответа не 200'
    print('udallllllllLLLLLLLLLLLLLLLLLL')





async def test_get_submenu_count2(ac: AsyncClient):
    async with async_session_maker() as session:
        query = select(submenu_table)
        result = await session.execute(query)
        res = result.all()
        print(res[0][0])

    async with async_session_maker() as session:
        query = select(submenu_table)
        result = await session.execute(query)
        res1 = result.all()
        print(res1[0][3])

    """Изменение текущего меню."""
    response = await ac.get(f"/api/v1/menus/{res1[0][3]}/submenus/{res[0][0]}")

    assert response.json()['dishes_count'] == 1, \
        'Количество блюд не соответствует ожидаемому'