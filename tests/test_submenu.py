import pytest
from sqlalchemy import insert, select
from conftest import ac, client, async_session_maker
from src.submenu.models import submenu_table
from src.menu.models import menu_table
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


async def test_get_submenu(ac: AsyncClient):
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
        
    response = await ac.get(f"/api/v1/menus/{res1[0][3]}/submenus")
    # assert response.status_code == HTTPStatus.OK, \
        # 'Статус ответа не 200'
    assert response.json()[0][0] == str(res[0][0]), \
        'id_menu ошибочно'
    assert response.json()[0][2] == str(res[0][3]), \
        'id_submenu ошибочно'


async def test_get_submenu_one(ac: AsyncClient):
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

    assert 'id' in response.json(), 'Идентификатора меню нет в ответе'
    assert 'title' in response.json(), 'Названия меню нет в ответе'
    assert 'description' in response.json(), 'Описания меню нет в ответе'
    assert 'menu_id' in response.json(), 'Описания меню нет в ответе'
    assert response.json()['title'] == "My submenu 1", \
        'Название меню не соответствует ожидаемому'
    assert response.json()['description'] == "My submenu description 1", \
        'Описание меню не соответствует ожидаемому'


async def test_patch_menu(ac: AsyncClient):
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
    response = await ac.patch(f"/api/v1/menus/{res1[0][3]}/submenus/{res[0][0]}", json={
    "title": "My updated submenu 1",
    "description": "My updated submenu description 1"})

    assert response.status_code == HTTPStatus.OK, \
        'Статус ответа не 200'
    assert 'id' in response.json(), 'Идентификатора меню нет в ответе'
    assert 'title' in response.json(), 'Названия меню нет в ответе'
    assert 'description' in response.json(), 'Описания меню нет в ответе'
    assert response.json()['title'] == "My updated submenu 1", \
        'Название меню не соответствует ожидаемому'
    assert response.json()['description'] == "My updated submenu description 1", \
        'Описание меню не соответствует ожидаемому'


async def test_get_submenu_one_update(ac: AsyncClient):
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

    assert 'id' in response.json(), 'Идентификатора меню нет в ответе'
    assert 'title' in response.json(), 'Названия меню нет в ответе'
    assert 'description' in response.json(), 'Описания меню нет в ответе'
    assert 'menu_id' in response.json(), 'Описания меню нет в ответе'
    assert response.json()['title'] == "My updated submenu 1", \
        'Название меню не соответствует ожидаемому'
    assert response.json()['description'] == "My updated submenu description 1", \
        'Описание меню не соответствует ожидаемому'
    

async def test_delete_added_menu(ac: AsyncClient, added_submenu_data):
    submenu_id = str(added_submenu_data[0])
    menu_id = str(added_submenu_data[1])
    print(menu_id)
    print(submenu_id)
    async with async_session_maker() as session:
        query = select(menu_table)
        result = await session.execute(query)
        res = result.all()
        print(res)
    """Удаление текущего меню."""
    response = await ac.delete(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")
    assert response.status_code == HTTPStatus.OK, \
        'Статус ответа не 200'
    assert response.json()['title'] == 'My updated submenu 1', \
        'Название меню не соответствует ожидаемому'
    assert response.json()['description'] == 'My updated submenu description 1', \
        'Описание меню не соответствует ожидаемому'


async def test_get_deleted_menu(ac: AsyncClient, added_submenu_data):
    submenu_id = str(added_submenu_data[0])
    menu_id = str(added_submenu_data[1])
    print(menu_id)
    print(submenu_id)
    response = await ac.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")
    assert response.status_code == HTTPStatus.NOT_FOUND, \
        'Статус ответа не 404'
    assert response.json()['detail'] == 'submenu not found', \
        'Сообщение об ошибке не соответствует ожидаемому'

