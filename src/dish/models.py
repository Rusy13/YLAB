# submenu/models.py
from sqlalchemy import Table, Column, Integer, MetaData, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship
import uuid
from src.submenu.models import submenu_table

# Base = declarative_base()
from src.database import Base
metadata = MetaData()

# в файле dish/models.py добавьте импорт таблицы submenus

dish_table = Table(
    "dishes",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False),
    Column("title", String, index=True),
    Column("description", String),
    Column("price", Integer),
    Column("submenu_id", UUID(as_uuid=True), ForeignKey(submenu_table.c.id)),  # исправлено на использование submenu_table
)
