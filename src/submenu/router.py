from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import crud, schemas
from src.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession

submenu_router = APIRouter()

@submenu_router.post("/{menu_id}/submenus", status_code=status.HTTP_201_CREATED, response_model=schemas.SubMenu)
async def create_submenu(menu_id: schemas.UUID, submenu: schemas.SubMenuCreate, db: Session = Depends(get_async_session)):
    return await crud.create_submenu(db, submenu, menu_id)

@submenu_router.get("/{menu_id}/submenus", response_model=list[schemas.SubMenu])
async def read_submenus(menu_id: schemas.UUID, db: Session = Depends(get_async_session)):
    return await crud.get_submenus(db, menu_id)



@submenu_router.get("/{menu_id}/submenus/{submenu_id}", response_model=schemas.SubMenu)
async def read_submenu(menu_id: schemas.UUID, submenu_id: schemas.UUID, db: AsyncSession = Depends(get_async_session)):
    return await crud.get_submenu(db, submenu_id)



@submenu_router.patch("/{menu_id}/submenus/{submenu_id}", response_model=schemas.SubMenuOutput)
async def update_submenu(menu_id: schemas.UUID, submenu_id: schemas.UUID, submenu: schemas.SubMenuCreate, db: AsyncSession = Depends(get_async_session)):
    return await crud.update_submenu(db, submenu_id, submenu)



@submenu_router.delete("/{menu_id}/submenus/{submenu_id}", response_model=schemas.SubMenu)
async def delete_submenu(menu_id: schemas.UUID, submenu_id: schemas.UUID, db: AsyncSession = Depends(get_async_session)):
    return await crud.delete_submenu(db, menu_id, submenu_id)
