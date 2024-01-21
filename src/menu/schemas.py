# menu/schemas.py
from pydantic import BaseModel
from typing import List
from uuid import UUID
from src.submenu.schemas import SubMenu  # Импорт SubMenu из правильного пути

class MenuBase(BaseModel):
    pass

class MenuCreate(MenuBase):
    title: str
    description: str

class Menu(MenuBase):
    id: UUID
    title: str  # Добавить атрибут name
    submenus: List[SubMenu] = []
    dishes_count: int
    submenus_count: int
    class Config:
        orm_mode = True
