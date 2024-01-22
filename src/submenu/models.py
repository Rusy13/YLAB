from sqlalchemy import Table, Column, Integer, MetaData, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship
import uuid
from src.database import Base
from src.menu.models import menu_table


metadata = MetaData()


submenu_table = Table(
    "submenus",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False),
    Column("title", String, index=True),
    Column("description", String),
    Column("menu_id", UUID(as_uuid=True), ForeignKey(menu_table.c.id)),
)
