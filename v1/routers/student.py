"""Router for student endpoints."""

from fastapi_crudrouter import SQLAlchemyCRUDRouter

from database import db_session
from models import Student
from v1.schemas.students import StudentCreate, StudentORM, StudentUpdate


router = SQLAlchemyCRUDRouter(
    schema=StudentORM,
    create_schema=StudentCreate,
    update_schema=StudentUpdate,
    db_model=Student,
    db=db_session,
)
