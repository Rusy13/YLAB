import os
from sqlalchemy import create_engine, MetaData
# from src.database import database_url
from src.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER
database_url = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
# from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine


engine = create_engine(database_url)

metadata = MetaData()
metadata.reflect(bind=engine)
metadata.drop_all(bind=engine)

print("База данных успешно очищена.")
