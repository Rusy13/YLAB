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
    title: str 
    price: str
    description: str

    class Config:
        orm_mode = True


class DishOutput(DishBase):
    id: UUID
    title: str 
    description: str
    price: str