from fastapi import FastAPI
from src.menu.router import menu_router
from src.submenu.router import submenu_router
from src.dish.router import dish_router
from src.database import async_engine
from src.menu.models import Base as MenuBase
from src.submenu.models import Base as SubMenuBase
from src.dish.models import Base as DishBase
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

app = FastAPI()
async_session_maker = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)


async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(MenuBase.metadata.create_all)
        await conn.run_sync(SubMenuBase.metadata.create_all)
        await conn.run_sync(DishBase.metadata.create_all)


@app.on_event("startup")
async def startup_event():
    await create_tables()


app.include_router(menu_router, prefix="/api/v1/menus", tags=["menus"])
app.include_router(submenu_router, prefix="/api/v1/menus", tags=["submenus"])
app.include_router(dish_router, prefix="/api/v1/menus", tags=["dishes"])