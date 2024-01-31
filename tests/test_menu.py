import pytest
from sqlalchemy import insert, select
from conftest import ac, client, async_session_maker
from src.submenu.models import submenu_table
from src.menu.models import menu_table
from conftest import async_session_maker
from http import HTTPStatus
from typing import Any
from httpx import AsyncClient


async def test_all_menu_empty(ac: AsyncClient):
    """Проверка получения пустого списка меню."""
    response = await ac.get("/api/v1/menus")
    assert response.status_code == 200, "Статус ответа не 200"
    data = response.json()
    assert data == [], "Тело ответа не пустое"


async def test_post_menu(ac: AsyncClient):
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


async def test_all_menu_not_empty(ac: AsyncClient):
    """Проверка получения непустого списка меню."""
    response = await ac.get("/api/v1/menus")
    assert response.status_code == HTTPStatus.OK, \
        'Статус ответа не 200'
    assert response.json() != [], 'В ответе пустой список'


async def test_patch_menu(ac: AsyncClient):
    async with async_session_maker() as session:
        query = select(menu_table)
        result = await session.execute(query)
        res = result.all()
        print(res[0][0])
    """Изменение текущего меню."""
    response = await ac.patch(f"/api/v1/menus/{res[0][0]}", json={
    "title": "My updated menu 1",
    "description": "My updated menu description 1"})

    assert response.status_code == HTTPStatus.OK, \
        'Статус ответа не 200'
    assert 'id' in response.json(), 'Идентификатора меню нет в ответе'
    assert 'title' in response.json(), 'Названия меню нет в ответе'
    assert 'description' in response.json(), 'Описания меню нет в ответе'
    assert response.json()['title'] == "My updated menu 1", \
        'Название меню не соответствует ожидаемому'
    assert response.json()['description'] == "My updated menu description 1", \
        'Описание меню не соответствует ожидаемому'


async def test_get_patched_menu(ac: AsyncClient):
    async with async_session_maker() as session:
        query = select(menu_table)
        result = await session.execute(query)
        res = result.all()
    """Получение обновленного меню."""
    query = select(menu_table)
    response = await ac.get(f"/api/v1/menus/{res[0][0]}")
    query = select(menu_table)
    assert response.status_code == HTTPStatus.OK, 'Статус ответа не 200'
    assert 'id' in response.json(), 'Идентификатора меню нет в ответе'
    assert response.json()['title'] == res[0][1], \
        'Название меню не соответствует ожидаемому'
    assert response.json()['description'] == res[0][2], \
        'Описание меню не соответствует ожидаемому'
    assert response.json()['submenus_count'] == 0, \
        'Количество подменю не соответствует ожидаемому'
    assert response.json()['dishes_count'] == 0, \
        'Количество блюд не соответствует ожидаемому'


async def test_delete_added_menu(ac: AsyncClient, added_menu_data):
    menu_id = added_menu_data[0]
    async with async_session_maker() as session:
        query = select(menu_table)
        result = await session.execute(query)
        res = result.all()
    """Удаление текущего меню."""
    response = await ac.delete(f"/api/v1/menus/{menu_id}")
    assert response.status_code == HTTPStatus.OK, \
        'Статус ответа не 200'
    assert response.json()['title'] == res[0][1], \
        'Название меню не соответствует ожидаемому'
    assert response.json()['description'] == res[0][2], \
        'Описание меню не соответствует ожидаемому'


async def test_get_deleted_menu(ac: AsyncClient, added_menu_data):
    menu_id = added_menu_data[0]
    print(menu_id)
    response = await ac.get(f"/api/v1/menus/{menu_id}")
    assert response.status_code == HTTPStatus.NOT_FOUND, \
        'Статус ответа не 404'
    assert response.json()['detail'] == 'menu not found', \
        'Сообщение об ошибке не соответствует ожидаемому'