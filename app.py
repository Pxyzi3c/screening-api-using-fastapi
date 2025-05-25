import re
import logging
from typing import List

from sqlalchemy.engine import URL

from rapidfuzz import fuzz
from fastapi import FastAPI, Query, Request, HTTPException
from fastapi.responses import ORJSONResponse
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND

from routes.screening import router as screening_router

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
screening_app.include_router(screening_router)