# crud.py

from fastapi.responses import JSONResponse
from sqlalchemy import UUID, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.menu.models import menu_table
from src.submenu.crud import delete_submenu
from src.submenu.models import submenu_table
from src.dish.models import dish_table
from . import models, schemas
from fastapi import HTTPException, Response, status


async def create_menu(db: AsyncSession, menu: schemas.MenuCreate):
    db_menu = menu_table.insert().values(**menu.dict())
    await db.execute(db_menu)
    await db.commit()

    # Get the last inserted menu
    result = await db.execute(select(menu_table).order_by(menu_table.c.id.desc()).limit(1))
    created_menu = result.fetchone()

    # Ensure that the required fields are present in the created_menu dictionary
    created_menu_with_counts = {
        'id': str(created_menu[0]),
        'name': created_menu[1],
        'description': created_menu[2],
        # 'description': 'undefined',
        'dishes_count': 0,  # Замените на актуальное значение
        'submenus_count': 0,  # Замените на актуальное значение
        'title': created_menu[1],  # Замените на актуальное значение
        # 'title': 'My title',  # Замените на актуальное значение

    }

    # Commit again to ensure that the changes are persisted
    await db.commit()

    # Return the created menu object
    return JSONResponse(content=created_menu_with_counts, status_code=201)
    # return created_menu_with_counts






async def get_menus(db: AsyncSession):
    result = await db.execute(select(menu_table))
    menus = result.all()

    menus_with_counts = []
    for menu in menus:
        submenus_count = await db.execute(select(func.count()).where(submenu_table.c.menu_id == menu.id))
        submenus_count = submenus_count.scalar()

        dishes_count = await db.execute(
            select(func.count()).where(dish_table.c.submenu_id.in_(select(submenu_table.c.id).where(submenu_table.c.menu_id == menu.id)))
        )
        dishes_count = dishes_count.scalar()

        menu_dict = {
            "id": str(menu.id),
            "title": menu.title,
            "description": menu.description,
            "submenus_count": submenus_count,
            "dishes_count": dishes_count,
            "submenus": []
        }

        menus_with_counts.append(menu_dict)

    return menus_with_counts
    # return []
    # return Response(status='OK')   
    # result = await db.execute(select(menu_table))
    # menus = result.all()

    # return menus_with_counts




async def get_menu(db: AsyncSession, menu_id: schemas.UUID):
    submenus_count = await db.execute(select(func.count()).where(submenu_table.c.menu_id == menu_id))
    submenus_count = submenus_count.scalar()

    dishes_count = await db.execute(
        select(func.count())
        .where(dish_table.c.submenu_id.in_(select(submenu_table.c.id).where(submenu_table.c.menu_id == menu_id)))
    )
    dishes_count = dishes_count.scalar()

    result = await db.execute(select(menu_table).where(menu_table.c.id == menu_id))
    menu = result.fetchone()

    if menu:
        menu_dict = {
            "id": str(menu.id),
            "title": menu.title,
            "description": menu.description,
            # "title": None,
            # "description": None,
            "submenus_count": submenus_count,
            "dishes_count": dishes_count
        }
        return menu_dict
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="menu not found")






async def update_menu(db: AsyncSession, menu_id: schemas.UUID, menu: schemas.MenuCreate):
    await db.execute(
        menu_table.update().where(menu_table.c.id == menu_id).values(title=menu.title, description = menu.description)
    )
    await db.commit()
    result = await db.execute(select(menu_table).where(menu_table.c.id == menu_id))
    menu = result.fetchone()
    if menu:
        menu_dict2 = {
            "id": str(menu.id),
            "title":menu.title,
            "description":  menu.description,
            # "submenus_count": submenus_count,
            # "dishes_count": dishes_count
        }
        return menu_dict2
    # return await get_menu(db, menu_id)
    # return await menu_dict










from sqlalchemy import select

async def get_submenus_by_menu_id(db: AsyncSession, menu_id: schemas.UUID):
    # Создаем запрос для выбора идентификаторов подменю связанных с меню
    query = select(submenu_table.c.id).where(submenu_table.c.menu_id == menu_id)

    # Исполняем запрос и получаем результат
    result = await db.execute(query)

    # Извлекаем идентификаторы из результата
    submenu_ids = [row[0] for row in result.fetchall()]

    return submenu_ids


async def delete_menu(db: AsyncSession, menu_id: schemas.UUID):
    db_menu = await get_menu(db, menu_id)
    
    if db_menu:
        # Получаем связанные подменю
        related_submenus = await get_submenus_by_menu_id(db, menu_id)

        # Удаляем связанные подменю
        for submenu_id in related_submenus:
            await delete_submenu(db, menu_id, submenu_id)

        # Затем удаляем само меню
        await db.execute(menu_table.delete().where(menu_table.c.id == menu_id).execution_options(synchronize_session="fetch"))

        # Осуществляем коммит транзакции
        await db.commit()
        return db_menu  # Возвращаем удаленный объект меню
    else:
        return None  # Возвращаем None, если меню не найдено

