import re
import logging
from typing import List

from fastapi import APIRouter, Query, HTTPException, status
from database.database import get_consolidated_sanctions
from schemas.sanction import SanctionSchema

from core.fuzz_ratio import get_name_similarity
from core.utils import get_full_name, standardize_name

logger = logging.getLogger("screening_api")
router = APIRouter()

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