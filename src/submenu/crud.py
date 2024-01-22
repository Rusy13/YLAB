from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session
from src.dish.crud import delete_dish
from . import models, schemas
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.submenu.models import submenu_table
from src.dish.models import dish_table
from src.menu.models import menu_table
from fastapi.responses import JSONResponse


async def create_submenu(db: AsyncSession, submenu: schemas.SubMenuCreate, menu_id: schemas.UUID):
    submenu_data = submenu.dict(exclude={"id", "menu_id"})
    db_submenu = submenu_table.insert().returning(submenu_table).values(**submenu_data, menu_id=menu_id)
    result = await db.execute(db_submenu)
    created_submenu = result.fetchone()
    await db.commit()
    return created_submenu


async def get_submenus(db: AsyncSession, menu_id: schemas.UUID):
    result = await db.execute(select(submenu_table).where(submenu_table.c.menu_id == menu_id))
    submenus = result.all()
    submenus_with_schema = [(str(submenu.id), submenu.title, str(submenu.menu_id)) for submenu in submenus]
    return JSONResponse(content=submenus_with_schema)


async def get_submenu(db: AsyncSession, submenu_id: schemas.UUID):
    print(f"Trying to fetch submenu with ID: {submenu_id}")
    result = await db.execute(select(models.submenu_table).where(models.submenu_table.c.id == submenu_id))
    submenu = result.fetchone()
    if not submenu:
        print(f"Submenu with ID {submenu_id} not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="submenu not found")
    dishes_count = await db.execute(select(func.count()).where(dish_table.c.submenu_id == submenu.id))
    dishes_count = dishes_count.scalar()
    submenu_dict = {
        "id": str(submenu.id),
        "title": submenu.title,
        "description": submenu.description,
        "menu_id": str(submenu.menu_id),
        "dishes_count": dishes_count,
        "dishes": []
    }
    return submenu_dict


async def update_submenu(db: AsyncSession, submenu_id: schemas.UUID, submenu: schemas.SubMenuCreate):
    await db.execute(
        submenu_table.update().where(submenu_table.c.id == submenu_id).values(title=submenu.title, description = submenu.description)
    )
    await db.commit()
    result = await db.execute(select(submenu_table).where(submenu_table.c.id == submenu_id))
    submenu = result.fetchone()
    if submenu:
        submenu_dict = {
            "id": str(submenu.id),
            "title": submenu.title,
            "description": submenu.description,
        }
        return submenu_dict


async def get_dishes_by_submenu_id(db: AsyncSession, submenu_id: schemas.UUID):
    statement = select(dish_table).where(dish_table.c.submenu_id == submenu_id)
    result = await db.execute(statement)
    return result.scalars().all()


async def delete_submenu(db: AsyncSession, menu_id: schemas.UUID, submenu_id: schemas.UUID):
    db_submenu = await get_submenu(db, submenu_id)
    if db_submenu:
        related_dishes = await get_dishes_by_submenu_id(db, submenu_id)
        for dish_id in related_dishes:
            await delete_dish(db, dish_id)
        await db.execute(submenu_table.delete().where(submenu_table.c.id == submenu_id).execution_options(synchronize_session="fetch"))
        await db.commit()
        return db_submenu  
    else:
        return None