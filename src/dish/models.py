from sqlalchemy import Table, Column, Integer, MetaData, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship
import uuid
from src.submenu.models import submenu_table
from src.database import Base, metadata


# metadata = MetaData()


dish_table = Table(
    "dishes",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False),
    Column("title", String, index=True),
    Column("description", String),
    Column("price", String),
    Column("submenu_id", UUID(as_uuid=True), ForeignKey(submenu_table.c.id)),
)
