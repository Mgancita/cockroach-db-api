"""Student schemas."""

from datetime import datetime
from typing import Optional
import uuid

from pydantic import BaseModel, EmailStr, Field, UUID4
from v1.schemas import PropertyBaseModel

class StudentBase(BaseModel):
    """Base schema for Students."""

    name: str
    email: EmailStr
    is_active: bool
    years_in_school: int
    major: str


class StudentCreate(StudentBase):
    """Schema for creating a Student."""

    pass


class StudentUpdate(BaseModel):
    """Schema for updating a Student."""

    name: Optional[str]
    email: Optional[EmailStr]
    is_active: Optional[bool]
    years_in_school: Optional[int]
    major: Optional[str]


class StudentORM(StudentBase):
    """Schema for Students."""

    id: UUID4
    created_at: datetime
    updated_at: datetime

    class Config:
        """Config for Student."""

        orm_mode = True
