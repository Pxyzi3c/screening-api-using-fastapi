from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.engine import URL

import os
from typing import Generator
import pandas as pd

# -------------------------------
# Environment Loader (robust)
# -------------------------------
def get_env_var(key: str) -> str:
    value = os.getenv(key)
    if value is None:
        raise EnvironmentError(f"Environment variable '{key}' is missing.")
    return value

# -------------------------------
# PostgreSQL Connection URL
# -------------------------------
DATABASE_URL = URL.create(
    drivername="postgresql+psycopg2",
    host=get_env_var("DB_HOST"),
    port=get_env_var("DB_PORT"),
    database=get_env_var("DB_NAME"),
    username=get_env_var("DB_USER"),
    password=get_env_var("DB_PASS"),
)

# -------------------------------
# Engine & Session Factory
# -------------------------------
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# -------------------------------
# Dependency for FastAPI
# -------------------------------
def get_db() -> Generator[Session, None, None]:
    """
    Yields a database session to be used in FastAPI routes.
    Ensures clean-up after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------------
# DB Query (used by API logic)
# -------------------------
def get_consolidated_sanctions() -> pd.DataFrame:
    return pd.read_sql("SELECT * FROM ofac_consolidated", con=engine)