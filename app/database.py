# database.py
import logging
import time
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import OperationalError

from app.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

SQLALCHEMY_DATABASE_URL = settings.POSTGRES_URL

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    echo=settings.DEBUG,  # Use settings.DEBUG to control SQL echo
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():

    max_retries = 5
    retry_delay = 5  # seconds

    for i in range(max_retries):
        try:
            logging.info("Attempting to connect to the database...")
            Base.metadata.create_all(bind=engine)
            logging.info("Database tables created successfully.")
            return
        except OperationalError as e:
            logging.error(f"Database connection failed: {e}")
            if i < max_retries - 1:
                logging.info(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                logging.critical(
                    "Failed to connect to the database after multiple attempts.")
                raise e

        except Exception as e:
            logging.critical(
                f"An unexpected error occurred during database initialization: {e}")
            raise e
