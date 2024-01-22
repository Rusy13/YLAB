# dish/schemas.py
from pydantic import BaseModel
from uuid import UUID

class DishBase(BaseModel):
    pass

class DishCreate(DishBase):
    title: str
    price: str
    description: str

class Dish(DishBase):
    id: UUID
    title: str  # Добавить атрибут name
    price: str
    description: str

    class Config:
        orm_mode = True




class DishOutput(DishBase):
    id: UUID
    title: str  # Добавить атрибут name
    description: str
    price: str
    # title: str  # Добавить атрибут name
    # submenus: List[SubMenu] = []
    # dishes_count: int
    # submenus_count: int