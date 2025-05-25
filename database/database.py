from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL

from os import environ

def load_env_variable(key: str) -> str:
    value = environ.get(key)

    if not value:
        raise RuntimeError(f"Missing environment variable: {key}")
    return value

connection_string = URL.create(
    drivername="postgresql+psycopg2",
    database=load_env_variable("DB_NAME"),
    host=load_env_variable("DB_HOST"),
    port=load_env_variable("DB_PORT"),
    username=load_env_variable("DB_USER"),
    password=load_env_variable("DB_PASS"),
)

"""
The engine manages the connection to the database and handles query execution.
"""
engine = create_engine(connection_string)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Database dependency for routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()