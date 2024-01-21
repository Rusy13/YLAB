# submenu/models.py
from sqlalchemy import Table, Column, Integer, MetaData, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship
import uuid

# Base = declarative_base()
from src.database import Base
metadata = MetaData()

# в файле submenu/models.py добавьте импорт таблицы menus
from src.menu.models import menu_table

submenu_table = Table(
    "submenus",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False),
    Column("title", String, index=True),
    Column("description", String),
    Column("menu_id", UUID(as_uuid=True), ForeignKey(menu_table.c.id)),  # исправлено на использование menu_table
)
