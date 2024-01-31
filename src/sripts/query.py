from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import sessionmaker
import sys
from pathlib import Path

# Получаем абсолютный путь к корневой директории проекта
project_root = Path("~/Desktop/UNIV/YLAB/DZ1/DZNEW/YLAB").expanduser().resolve()

# Добавляем путь к корневой директории в sys.path
sys.path.append(str(project_root))

# Теперь вы можете импортировать модули из вашего проекта
from src.menu.models import menu_table
from src.submenu.models import submenu_table
from src.dish.models import dish_table


import asyncio
from sqlalchemy import func
from src.menu.models import menu_table
from src.submenu.models import submenu_table
from src.dish.models import dish_table
from src.database import get_async_session

from sqlalchemy import func
from src.menu.models import menu_table
from src.submenu.models import submenu_table
from tests.conftest import async_session_maker

from asyncio import sleep
import pytest
from sqlalchemy import insert, select
from tests.conftest import ac, client, async_session_maker
from src.submenu.models import submenu_table
from src.menu.models import menu_table
from src.dish.models import dish_table

from tests.conftest import async_session_maker
from http import HTTPStatus
from typing import Any
from httpx import AsyncClient
from sqlalchemy import func, select
# from src.menu.models import menu_table, submenu_table, dish_table
from src.database import async_session_maker

async def count_submenus_and_dishes():
    async with async_session_maker() as session:
        # Строим запрос для подсчета количества подменю и блюд для каждого меню
        query = (
            select(
                menu_table.c.id,
                menu_table.c.title,
                func.count(submenu_table.c.id).label('submenu_count'),
                func.count(dish_table.c.id).label('dish_count')
            )
            .select_from(menu_table)
            .outerjoin(submenu_table, submenu_table.c.menu_id == menu_table.c.id)
            .outerjoin(dish_table, dish_table.c.submenu_id == submenu_table.c.id)
            .group_by(menu_table.c.id, menu_table.c.title)
        )

        # Выполняем запрос
        result = await session.execute(query)
        rows = result.fetchall()

        # Выводим результаты
        for row in rows:
            menu_id, menu_title, submenu_count, dish_count = row
            print(f"Menu ID: {menu_id}, Name: {menu_title}, Submenu Count: {submenu_count}, Dish Count: {dish_count}")

# Пример использования
async def main():
    await count_submenus_and_dishes()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())