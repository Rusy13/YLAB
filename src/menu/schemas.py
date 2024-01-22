# menu/schemas.py
from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID
from src.submenu.schemas import SubMenu  # Импорт SubMenu из правильного пути

class MenuBase(BaseModel):
    pass

class MenuCreate(MenuBase):
    title: str
    description: str

class Menu(MenuBase):
    id: UUID
    title: Optional[str]  # Добавить атрибут name
    description: Optional[str]
    submenus: List[SubMenu] = []
    dishes_count: int
    submenus_count: int
    class Config:
        orm_mode = True



class MenuOutput(MenuBase):
    id: UUID
    title: str  # Добавить атрибут name
    description: Optional[str]
    # submenus: List[SubMenu] = []
    # dishes_count: int
    # submenus_count: int