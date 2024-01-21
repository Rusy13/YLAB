# submenu/crud.py
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








async def create_submenu(db: AsyncSession, submenu: schemas.SubMenuCreate, menu_id: schemas.UUID):
        # Exclude "id" and "menu_id" from the submenu data
    submenu_data = submenu.dict(exclude={"id", "menu_id"})

    # Use the returning clause to get the values of the inserted row
    db_submenu = submenu_table.insert().returning(submenu_table).values(**submenu_data, menu_id=menu_id)

    result = await db.execute(db_submenu)
    created_submenu = result.fetchone()

    await db.commit()
    # return created_submenu
    return JSONResponse(content = 'Success', status_code=201)














from fastapi.responses import JSONResponse

async def get_submenus(db: AsyncSession, menu_id: schemas.UUID):
    result = await db.execute(select(submenu_table).where(submenu_table.c.menu_id == menu_id))
    submenus = result.all()

    # Возвращаем кортежи с нужными значениями
    submenus_with_schema = [(str(submenu.id), submenu.title, str(submenu.menu_id)) for submenu in submenus]

    return JSONResponse(content=submenus_with_schema)








async def get_submenu(db: AsyncSession, submenu_id: schemas.UUID):
    print(f"Trying to fetch submenu with ID: {submenu_id}")
    result = await db.execute(select(models.submenu_table).where(models.submenu_table.c.id == submenu_id))
    submenu = result.fetchone()
    # submenus_count = await db.execute(select(func.count()).where(submenu_table.c.submenu_id == submenu_id))
    # submenus_count = submenus_count.scalar()

    # dishes_count = await db.execute(
    #     select(func.count())
    #     .where(dish_table.c.submenu_id.in_(select(submenu_table.c.id).where(submenu_table.c.submenu_id == submenu_id)))
    # )
    # dishes_count = dishes_count.scalar()


    dishes_count = await db.execute(
        select(func.count()).where(dish_table.c.submenu_id == submenu.id))
    dishes_count = dishes_count.scalar()


    if submenu:
        submenu_dict = {
            "id": str(submenu.id),
            "title": submenu.title,
            "description": submenu.description,
            "menu_id": str(submenu.menu_id),
            "dishes_count": dishes_count,  # Добавление dishes_count к результату
            # "submenus_count": submenus_count,
            "dishes": []
        }
        return submenu_dict
    else:
        print(f"Submenu with ID {submenu_id} not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="submenu not found")





# Ваши импорты
async def update_submenu(db: AsyncSession, submenu_id: schemas.UUID, submenu: schemas.SubMenuCreate):
    await db.execute(
        submenu_table.update().where(submenu_table.c.id == submenu_id).values(title=submenu.title)
    )
    await db.commit()
    return await get_submenu(db, submenu_id)

async def get_dishes_by_submenu_id(db: AsyncSession, submenu_id: schemas.UUID):
    statement = select(dish_table).where(dish_table.c.submenu_id == submenu_id)
    result = await db.execute(statement)
    return result.scalars().all()

async def delete_submenu(db: AsyncSession, menu_id: schemas.UUID, submenu_id: schemas.UUID):
    db_submenu = await get_submenu(db, submenu_id)
    if db_submenu:
        # Получаем связанные блюда
        related_dishes = await get_dishes_by_submenu_id(db, submenu_id)

        # Удаляем связанные блюда
        for dish_id in related_dishes:
            await delete_dish(db, dish_id)

        # Затем удаляем само подменю
        await db.execute(submenu_table.delete().where(submenu_table.c.id == submenu_id).execution_options(synchronize_session="fetch"))

        # Осуществляем коммит транзакции
        await db.commit()
        return db_submenu  # Возвращаем удаленный объект
    else:
        return None  # Возвращаем None, если подменю не найдено