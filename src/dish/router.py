from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import crud, schemas
from src.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession


dish_router = APIRouter()


@dish_router.post("/{menu_id}/submenus/{submenu_id}/dishes", status_code=status.HTTP_201_CREATED, response_model=schemas.Dish)
async def create_dish(dish: schemas.DishCreate, submenu_id: schemas.UUID, db: AsyncSession = Depends(get_async_session)):
    return await crud.create_dish(db, dish, submenu_id)


@dish_router.get("/{menu_id}/submenus/{submenu_id}/dishes", response_model=List[schemas.Dish])
async def get_dishes(menu_id: schemas.UUID, submenu_id: schemas.UUID, db: AsyncSession = Depends(get_async_session)):
    return await crud.get_dishes(db, submenu_id)


@dish_router.get("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", response_model=schemas.Dish)
async def read_dish(dish_id: schemas.UUID, submenu_id: schemas.UUID, db: AsyncSession = Depends(get_async_session)):
    return await crud.get_dish(db, dish_id)


@dish_router.patch("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", response_model=schemas.DishOutput)
async def update_dish(dish_id: schemas.UUID, dish: schemas.DishCreate, db: Session = Depends(get_async_session)):
    return await crud.update_dish(db, dish_id, dish)


@dish_router.delete("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", response_model=schemas.Dish)
async def delete_dish(dish_id: schemas.UUID, db: AsyncSession = Depends(get_async_session)):
    return await crud.delete_dish(db, dish_id)