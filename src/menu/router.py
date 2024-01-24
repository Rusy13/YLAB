from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from . import crud, schemas
from src.database import get_async_session
from typing import List


menu_router = APIRouter()


@menu_router.post("/", response_model=schemas.Menu)
async def create_menu(menu: schemas.MenuCreate, db: AsyncSession = Depends(get_async_session)):
    return await crud.create_menu(db, menu)


@menu_router.get("/", response_model=List[schemas.Menu])
async def read_menus(db: AsyncSession = Depends(get_async_session)):
    return await crud.get_menus(db)


@menu_router.get("/{menu_id}", response_model=schemas.Menu)
async def read_menu(menu_id: schemas.UUID, db: AsyncSession = Depends(get_async_session)):
    return await crud.get_menu(db, menu_id)


@menu_router.patch("/{menu_id}", response_model=schemas.MenuOutput)
async def update_menu(menu_id: schemas.UUID, menu: schemas.MenuCreate, db: AsyncSession = Depends(get_async_session)):
    return await crud.update_menu(db, menu_id, menu)


@menu_router.delete("/{menu_id}", response_model=schemas.Menu)
async def delete_menu(menu_id: schemas.UUID, db: AsyncSession = Depends(get_async_session)):
    return await crud.delete_menu(db, menu_id)
