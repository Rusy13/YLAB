from sqlalchemy import func, select
import sys
from pathlib import Path

project_root = Path("~/Desktop/UNIV/YLAB/DZ1/DZNEW/YLAB").expanduser().resolve()

sys.path.append(str(project_root))

import asyncio
from sqlalchemy import func
from src.menu.models import menu_table
from src.submenu.models import submenu_table
from src.dish.models import dish_table
from sqlalchemy import select
from tests.conftest import async_session_maker
from sqlalchemy import func, select
from src.database import async_session_maker

async def count_submenus_and_dishes():
    async with async_session_maker() as session:
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

        result = await session.execute(query)
        rows = result.fetchall()
        if not rows:
            print("Нет данных в базе.")
        else:
            for row in rows:
                menu_id, menu_title, submenu_count, dish_count = row
                print(f"Menu ID: {menu_id}, Name: {menu_title}, Submenu Count: {submenu_count}, Dish Count: {dish_count}")

async def main():
    await count_submenus_and_dishes()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())