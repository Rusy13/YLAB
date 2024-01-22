from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID
from src.submenu.schemas import SubMenu  


class MenuBase(BaseModel):
    pass


class MenuCreate(MenuBase):
    title: str
    description: str


class Menu(MenuBase):
    id: UUID
    title: Optional[str] 
    description: Optional[str]
    submenus: List[SubMenu] = []
    dishes_count: int
    submenus_count: int
    class Config:
        orm_mode = True


class MenuOutput(MenuBase):
    id: UUID
    title: str 
    description: Optional[str]