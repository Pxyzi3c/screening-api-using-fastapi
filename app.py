import re
import logging
import pandas as pd
from os import environ
from typing import List, Optional

from sqlalchemy import create_engine
from sqlalchemy.engine import URL

from rapidfuzz import fuzz
from fastapi import FastAPI, Query, Request, HTTPException
from fastapi.responses import ORJSONResponse
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY
from pydantic import BaseModel

from database.database import get_consolidated_sanctions

# -----------------------------
# Response Schema
# -----------------------------

class Sanction(BaseModel):
    ent_num: int
    sdn_name: str
    sdn_type: str
    complete_address: str
    country: str
    add_remarks: str
    cleaned_name: str
    similarity_score: Optional[float]

# -----------------------------
# App Initialization
# -----------------------------

screening_app = FastAPI(
    title="OFAC Sanctions Screening API",
    version="0.0.1",
    default_response_class=ORJSONResponse
)

# -----------------------------
# Logging Configuration
# -----------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger("screening_api")

# -----------------------------
# Utility Functions
# -----------------------------
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
    except Exception as e:
        logger.warning(f"Similarity comparison failed: {e}")
        return None

def get_full_name(fname: str, lname: str):
    return f"{fname.title()} {lname.title()}"

# -----------------------------
# Request Logging Middleware
# -----------------------------

@screening_app.middleware("http")
async def log_requests(request: Request, call_next):
    request_id = id(request)
    logger.info(f"[REQ {request_id}] {request.method} {request.url}")
    
    response = await call_next(request)

    logger.info(f"[RES] {request_id} Status: {response.status_code}")
    return response

# -----------------------------
# Routes
# -----------------------------

@screening_app.get("/", status_code=HTTP_200_OK)
async def root():
    name = get_full_name("Harvy Jones", "Pontillas")

    return {
        "status": "success",
        "response": {
            "name": name,
            "app_title": screening_app.title,
            "version": screening_app.version
        }
    }
    
@screening_app.get("/screen", response_model=List[Sanction], status_code=HTTP_200_OK)
async def screen(
    name: str = Query(..., example="AEROCARIBBEAN AIRLINES"), 
    threshold: float = Query(0.7, ge=0.0, le=1.0)
) :
    cleaned_name = standardize_name(name)
    sanctions = get_consolidated_sanctions()
    print(sanctions.head())
    
    # Sanction name
    sanctions["similarity_score"] = sanctions["cleaned_name"].apply(
        get_name_similarity, args=(cleaned_name,))
    
    filtered_sanctions = sanctions[sanctions["similarity_score"] >= threshold]
    result = filtered_sanctions.fillna("-").to_dict(orient="records")

    logger.info(f"[SCREEN] Input: {name}, Threshold: {threshold}, Results: {len(result)}")

    if len(result) == 0:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="No sanctions found"
        )
    
    return result