import re
import logging
from typing import List, Optional

import pandas as pd
from fastapi import APIRouter, Query, HTTPException, status
from database.database import get_consolidated_sanctions
from schemas.sanction import SanctionSchema
from rapidfuzz import fuzz

logger = logging.getLogger("screening_api")
router = APIRouter()

# -----------------------------
# Utility Functions (can move to core later)
# -----------------------------

def standardize_name(name: str) -> str:
    clean_name = re.sub(r"[/-]", " ", name).upper()
    clean_name = re.sub(r"[^A-Z0-9\s]", "", clean_name)
    clean_name = re.sub(r"\s+", " ", clean_name).strip()
    return clean_name

def get_name_similarity(name1: str, name2: str, sort_names: bool = False) -> Optional[float]:
    if sort_names:
        name1 = " ".join(sorted(name1.split()))
        name2 = " ".join(sorted(name2.split()))
    try:
        return round(fuzz.ratio(name1, name2) / 100, 2)
    except Exception as e:
        logger.warning(f"Similarity comparison failed: {e}")
        return None

def get_full_name(fname: str, lname: str):
    return f"{fname.title()} {lname.title()}"

# -----------------------------
# Routes
# -----------------------------
@router.get("/", status_code=status.HTTP_200_OK)
async def root():
    name = get_full_name("Harvy Jones", "Pontillas")
    return {
        "status": "success",
        "response": {
            "name": name,
            "app_title": "OFAC Sanctions Screening API",
            "version": "0.0.1"
        }
    }

@router.get("/screen", response_model=List[SanctionSchema], status_code=status.HTTP_200_OK)
async def screen(
    name: str = Query(..., example="AEROCARIBBEAN AIRLINES"),
    threshold: float = Query(0.7, ge=0.0, le=1.0)
):
    cleaned_name = standardize_name(name)
    sanctions = get_consolidated_sanctions()

    sanctions["similarity_score"] = sanctions["cleaned_name"].apply(
        get_name_similarity, args=(cleaned_name,)
    )

    filtered = sanctions[sanctions["similarity_score"] >= threshold]
    result = filtered.fillna("-").to_dict(orient="records")

    logger.info(f"[SCREEN] Input: {name}, Threshold: {threshold}, Results: {len(result)}")

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No sanctions found"
        )

    return result