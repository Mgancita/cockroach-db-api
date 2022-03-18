"""Database session manager."""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import MetaData

from config import apisecrets, logger, testing

NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}
metadata = MetaData(naming_convention=NAMING_CONVENTION)

database_url = apisecrets.DATABASE_URL if not testing else apisecrets.TEST_URL
engine = create_engine(database_url, pool_pre_ping=True, pool_size=10, max_overflow=0)
SessionLocal = sessionmaker(autocommit=False, expire_on_commit=False, autoflush=True, bind=engine)
Base = declarative_base()


def db_session():
    """Create a database session with rollback."""
    try:
        db = SessionLocal()
        yield db
        db.commit()
    except Exception as e:
        logger.error("Exception raised, rolling back changes. " f"Exception: {e}.")
        db.rollback()
        raise e
    finally:
        db.close()
