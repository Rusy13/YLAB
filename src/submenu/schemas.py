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
    title: str
    description: Optional[str]
    menu_id: UUID
    dishes: List[Dish] = []  
    dishes_count: int = 0

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
        from_orm = True
        from_attributes = True


class SubMenuOutput(SubMenuBase):
    id: UUID
    title: str
    description: str