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










async def test_post_menu(ac: AsyncClient):
    """Добавление нового меню."""
    response = await ac.post("/api/v1/menus", json={
    "title": "My submenu 1",
    "description": "My submenu description 1"
})
    assert response.status_code == HTTPStatus.CREATED, \
        'Статус ответа не 201'
    assert 'id' in response.json(), 'Идентификатора меню нет в ответе'
    assert 'title' in response.json(), 'Названия меню нет в ответе'
    assert 'description' in response.json(), 'Описания меню нет в ответе'
    assert 'submenus_count' in response.json(), \
        'Количества подменю нет в ответе'
    assert 'dishes_count' in response.json(), 'Количества блюд нет в ответе'
    assert response.json()['title'] == "My submenu 1", \
        'Название меню не соответствует ожидаемому'
    assert response.json()['description'] == "My submenu description 1", \
        'Описание меню не соответствует ожидаемому'






async def test_post_submenu(ac: AsyncClient):
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











async def test_post_dish(ac: AsyncClient):
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
    




        
async def test_get_dish(ac: AsyncClient, added_submenu_data):
    submenu_id = str(added_submenu_data[0])
    menu_id = str(added_submenu_data[1])

    async with async_session_maker() as session:
        query = select(dish_table)
        result = await session.execute(query)
        res = result.all()
        print(res[0][0])
        
    response = await ac.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes")

    assert response.json() == [
    {
        "id": str(res[0][0]),
        "title": "My dish 1",
        "price": "12.5",
        "description": "My dish description 1"
    }
], \
        'dish не сходится'
    









async def test_get_dish2(ac: AsyncClient, added_submenu_data):
    submenu_id = str(added_submenu_data[0])
    menu_id = str(added_submenu_data[1])

    async with async_session_maker() as session:
        query = select(dish_table)
        result = await session.execute(query)
        res = result.all()
        print(res[0][0])
        
    response = await ac.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{res[0][0]}")

    assert response.json() == {
        "id": str(res[0][0]),
        "title": "My dish 1",
        "price": "12.5",
        "description": "My dish description 1"
    }, \
        'dish не сходится 2'
    






async def test_upd_dish2(ac: AsyncClient, added_submenu_data):
    submenu_id = str(added_submenu_data[0])
    menu_id = str(added_submenu_data[1])

    async with async_session_maker() as session:
        query = select(dish_table)
        result = await session.execute(query)
        res = result.all()
        print(res[0][0])
        
    response = await ac.patch(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{res[0][0]}", json={
    "title": "My updated dish 1",
    "description": "My updated dish description 1",
    "price": "14.50"})

    async with async_session_maker() as session:
        query = select(dish_table)
        result = await session.execute(query)
        res1 = result.all()
        print(res1[0][0])

    assert response.json() == {
        "id": str(res1[0][0]),
        "title": "My updated dish 1",
        "description": "My updated dish description 1",
        "price": "14.5"
    }, \
        'upd не проходит'
    








async def test_get_dish3(ac: AsyncClient, added_submenu_data):
    submenu_id = str(added_submenu_data[0])
    menu_id = str(added_submenu_data[1])

    async with async_session_maker() as session:
        query = select(dish_table)
        result = await session.execute(query)
        res = result.all()
        print(res[0][0])
        
    response = await ac.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{res[0][0]}")

    assert response.json() == {
        "id": str(res[0][0]),
        "title": "My updated dish 1",
        "price": "14.5",
        "description": "My updated dish description 1"
    }, \
        'dish не сходится 3'
    














async def test_delete_added_dish(ac: AsyncClient, added_dish_data, added_submenu_data):
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
    assert response.json()['title'] == "My updated dish 1", \
        'Название dsih не соответствует ожидаемому'
    assert response.json()['description'] == 'My updated dish description 1', \
        'Описание dish не соответствует ожидаемому'
    assert response.json()['price'] == '14.5', \
        'Цена dish не соответствует ожидаемому'












async def test_get_deleted_вшыр(ac: AsyncClient, added_submenu_data, added_dish_data):
    dish_id = str(added_dish_data[0])
    submenu_id = str(added_dish_data[1])
    menu_id = str(added_submenu_data[1])
    print(dish_id)
    print(submenu_id)
    print(menu_id)
    response = await ac.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
    assert response.status_code == HTTPStatus.NOT_FOUND, \
        'Статус ответа не 404'
    assert response.json()['detail'] == 'dish not found', \
        'Сообщение об ошибке не соответствует ожидаемому'

