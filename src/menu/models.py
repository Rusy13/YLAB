# menu/models.py
import uuid
from sqlalchemy import Table, Column, MetaData, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.database import Base
metadata = MetaData()

menu_table = Table(
    "menus",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False),
    Column("title", String, index=True),
    Column("description", String),
)
