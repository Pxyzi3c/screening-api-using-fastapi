import os
import pandas as pd
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.engine import URL

# --------------------------------------------------
# Environment Variable Loader (safe and minimal)
# --------------------------------------------------
def get_env_var(key: str) -> str:
    value = os.getenv(key)

    if value is None:
        raise EnvironmentError(f"Missing required environment variable: '{key}'")
    return value

# --------------------------------------------------
# PostgreSQL Connection URL Construction
# --------------------------------------------------
DATABASE_URL = URL.create(
    drivername="postgresql+psycopg2",
    host=get_env_var("DB_HOST"),
    port=get_env_var("DB_PORT"),
    database=get_env_var("DB_NAME"),
    username=get_env_var("DB_USER"),
    password=get_env_var("DB_PASS"),
)

# --------------------------------------------------
# SQLAlchemy Engine and Session Factory
# --------------------------------------------------
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# --------------------------------------------------
# Dependency for FastAPI Injection
# --------------------------------------------------
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

# --------------------------------------------------
# Public Data Query - Sanctions Table
# --------------------------------------------------
def get_consolidated_sanctions() -> pd.DataFrame:
    return pd.read_sql("SELECT * FROM ofac_consolidated", con=engine)