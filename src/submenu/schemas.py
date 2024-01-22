from pydantic import BaseModel, UUID4
from typing import List, Optional
from uuid import UUID
from src.dish.schemas import Dish

class SubMenuBase(BaseModel):
    pass

class SubMenuCreate(SubMenuBase):
    title: str
    description: str

class SubMenu(SubMenuBase):
    id: UUID
    title: str  # Добавить атрибут name
    # description: str
    description: Optional[str]
    menu_id: UUID
    dishes: List[Dish] = []  # Использование Dish напрямую
    dishes_count: int = 0
    # submenus_count: int
    # description: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
        # Установите from_orm и from_attributes оба в True
        from_orm = True
        from_attributes = True

    # submenu_dict = {
    #     "id": str(submenu.id),
    #     "title": submenu.title,
    #     "description": submenu.description,
    #     "menu_id": str(submenu.menu_id),
    #     "dishes_count": dishes_count,
    #     "dishes": []
    # }



class SubMenuOutput(SubMenuBase):
    id: UUID
    title: str  # Добавить атрибут name
    description: str
    # submenus: List[SubMenu] = []
    # dishes_count: int
    # submenus_count: int