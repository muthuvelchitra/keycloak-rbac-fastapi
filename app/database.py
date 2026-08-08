import psycopg2

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import settings
from app.core.logger import logger


# ============================================================
# DATABASE URL
# ============================================================

DATABASE_URL = settings.database_url


# ============================================================
# SQLAlchemy ENGINE
# ============================================================

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)


# ============================================================
# SESSION
# ============================================================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


# ============================================================
# BASE
# ============================================================

Base = declarative_base()


# ============================================================
# DATABASE DEPENDENCY
# ============================================================

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# ============================================================
# RAW POSTGRESQL CONNECTION
# ============================================================

def get_db_connection():

    return psycopg2.connect(
        host=settings.POSTGRES_HOST,
        port=settings.POSTGRES_PORT,
        database=settings.POSTGRES_DB,
        user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
    )


# ============================================================
# TEST DATABASE
# ============================================================

def test_database_connection() -> bool:

    connection = None

    try:

        connection = get_db_connection()

        logger.info(
            "PostgreSQL database connection successful"
        )

        return True

    except Exception as exc:

        logger.error(
            "PostgreSQL connection failed: %s",
            exc
        )

        return False

    finally:

        if connection:

            connection.close()


# ============================================================
# CREATE TABLES
# ============================================================

def create_users_table():

    try:

        # Import model before create_all
        from app.models import User  # noqa

        Base.metadata.create_all(
            bind=engine
        )

        logger.info(
            "Database tables created or already exist"
        )

    except Exception as exc:

        logger.error(
            "Database table creation failed: %s",
            exc
        )

        raise