import re
import pandas as pd
from os import environ
from sqlalchemy import create_engine, Engine
from sqlalchemy import URL
from rapidfuzz import fuzz
from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse

# App name
screening_app = FastAPI()

# Helper functions
def get_consolidated_sanctions() -> pd.DataFrame:
    # Get environment variables
    HOST = environ["DB_HOST"]
    PORT = environ["DB_PORT"]
    NAME = environ["DB_NAME"]
    USER = environ["DB_USER"]
    PASSWORD = environ["DB_PASS"]

    # Define connection string to PostgreSQL database
    connection_string = URL.create(
        drivername="postgresql+psycopg2",
        database=NAME,
        host=HOST,
        port=PORT,
        username=USER,
        password=PASSWORD
    )

    # Create engine object
    engine = create_engine(connection_string)

    # Query database
    df = pd.read_sql("SELECT * FROM ofac_consolidated", con=engine)

    return df

def standardize_name(name: str) -> str:
    clean_name = re.sub("[/-]", " ", name).upper()
    clean_name = re.sub("[^A-Z0-9\\s]", "", clean_name)
    clean_name = re.sub("\\s+", " ", clean_name).strip()
    return clean_name

def get_name_similarity(name1: str, name2: str, sort_names: bool = False) -> float | None:
    # Sort names if requested
    if sort_names:
        name1 = " ".join(sorted(name1.split(" ")))
        name2 = " ".join(sorted(name2.split(" ")))

    try:
        return round(fuzz.ratio(name1, name2) / 100, 2)
    except:
        return None

def get_full_name(fname: str, lname: str):
    full_name = fname.title() + " " + lname.title()
    return full_name

# Routes
@screening_app.get("/")
async def root():
    name = get_full_name("Harvy Jones", "Pontillas")
    result = {
        "status": "success",
        "response": {
            "name": name,
            "app_title": "Simple Screening API",
            "version": "0.0.1"
        }
    }
    
    return result

@screening_app.get("/screen")
async def screen(name: str, threshold: float = 0.7):
    cleaned_name = standardize_name(name)
    sanctions = get_consolidated_sanctions()
    
    # Sanction name
    sanctions["similarity_score"] = sanctions["cleaned_name"].apply(
        get_name_similarity, args=(cleaned_name,))
    filtered_sanctions = sanctions[sanctions["similarity_score"] >= threshold]
    
    result = filtered_sanctions.fillna("-").to_dict(orient="records")

    return {
        "status": "success",
        "response": result
    }