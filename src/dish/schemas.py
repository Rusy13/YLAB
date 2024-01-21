# dish/schemas.py
from pydantic import BaseModel
from uuid import UUID

class DishBase(BaseModel):
    pass

class DishCreate(DishBase):
    title: str
    price: float
    description: str

class Dish(DishBase):
    id: UUID
    title: str  # Добавить атрибут name
    price: float
    description: str

    class Config:
        orm_mode = True