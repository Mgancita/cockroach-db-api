"""Data models used by database for migrations, reading, and writing."""

from datetime import datetime
import uuid

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from database import Base


class Student(Base):
    """Database model for Students."""

    __tablename__ = "students"

    id = Column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        unique=True,
        primary_key=True,
        index=True,
        nullable=False,
    )

    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)

    is_active = Column(Boolean, nullable=False)
    years_in_school = Column(Integer, nullable=False)
    major = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
