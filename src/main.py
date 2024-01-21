# main.py
from fastapi import FastAPI
from src.menu.router import menu_router
from src.submenu.router import submenu_router
from src.dish.router import dish_router
from src.database import async_engine

app = FastAPI()

# Создание таблиц в базе данных
from src.menu.models import Base as MenuBase
from src.submenu.models import Base as SubMenuBase
from src.dish.models import Base as DishBase

# Импорт асинхронных инструментов
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

# Создание асинхронных сессий
async_session_maker = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

# Асинхронная функция для создания таблиц
async def create_tables():
    # Используйте async_engine здесь, а не async_session_maker
    async with async_engine.begin() as conn:
        await conn.run_sync(MenuBase.metadata.create_all)
        await conn.run_sync(SubMenuBase.metadata.create_all)
        await conn.run_sync(DishBase.metadata.create_all)

# Вызов асинхронной функции
@app.on_event("startup")
async def startup_event():
    await create_tables()

# Включение роутеров
app.include_router(menu_router, prefix="/api/v1/menus", tags=["menus"])
app.include_router(submenu_router, prefix="/api/v1/menus", tags=["submenus"])
app.include_router(dish_router, prefix="/api/v1/menus", tags=["dishes"])
