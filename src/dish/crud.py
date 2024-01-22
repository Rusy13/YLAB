# dish/crud.py
from sqlalchemy.orm import Session
from . import models, schemas
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from src.dish.models import dish_table
from sqlalchemy.future import select
from . import models
from fastapi import HTTPException, status


# dish/crud.py
from sqlalchemy import update
from fastapi.responses import JSONResponse

async def create_dish(db: AsyncSession, dish: schemas.DishCreate, submenu_id: UUID):
    try:
        # Exclude "id" and "submenu_id" from the dish data
        dish_data = dish.dict(exclude={"id", "submenu_id"})

        # Use the returning clause to get the values of the inserted row
        db_dish = models.dish_table.insert().returning(models.dish_table).values(submenu_id=submenu_id, **dish_data)

        result = await db.execute(db_dish)
        created_dish = result.fetchone()

        await db.commit()
        return created_dish
        # return JSONResponse(content=created_dish, status_code=201)
    except Exception as e:
        print(f"Error creating dish: {e}")
        await db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")





async def get_dishes(db: AsyncSession, submenu_id: schemas.UUID):
    result = await db.execute(select(dish_table).where(dish_table.c.submenu_id == submenu_id))
    dishes = result.all()

    # Check if dishes exist
    if not dishes:
        # Return an empty list or raise an exception based on your requirement
        return []

    # Return dishes as a list of dictionaries
    dishes_with_schema = [{"id": str(dish.id), "title": dish.title, "description": dish.description, "price": str(dish.price), "submenu_id": str(dish.submenu_id)} for dish in dishes]
    return dishes_with_schema





async def get_dish(db: AsyncSession, dish_id: UUID):
    result = await db.execute(select(dish_table).where(dish_table.c.id == dish_id))
    dish = result.first()  # Вместо result.scalar()

    if dish:
        dish_dict = {
            "id": str(dish.id),
            "title": dish.title,
            "description": dish.description,
            "price": dish.price,
            "submenu_id": str(dish.submenu_id),
        }
        return dish_dict
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="dish not found")


async def update_dish(db: AsyncSession, dish_id: schemas.UUID, dish: schemas.DishCreate):
    await db.execute(
        dish_table.update().where(dish_table.c.id == dish_id).values(title=dish.title, price=dish.price, description = dish.description)
    )
    await db.commit()
    result = await db.execute(select(dish_table).where(dish_table.c.id == dish_id))
    dish = result.fetchone()
    if dish:
        dish_dict = {
            "id": str(dish.id),
            "title": dish.title,
            "description": dish.description,
            "price": dish.price,
            # "submenus_count": submenus_count,
            # "dishes_count": dishes_count
        }
        return dish_dict
    # return await get_menu(db, menu_id)
    # return await menu_dict


    # return await get_dish(db, dish_id)
    return dish_dict









# crud.py
async def delete_dish(db: AsyncSession, dish_id: schemas.UUID):
    db_dish = await get_dish(db, dish_id)
    if db_dish:
        await db.execute(dish_table.delete().where(dish_table.c.id == dish_id))
        await db.commit()
        return db_dish
    else:
        return None