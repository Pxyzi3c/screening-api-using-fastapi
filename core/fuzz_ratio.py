from typing import Optional
from rapidfuzz import fuzz
import logging

logger = logging.getLogger("screening_api")

def get_name_similarity(name1: str, name2: str, sort_names: bool = False) -> Optional[float]:
    if sort_names:
        name1 = " ".join(sorted(name1.split()))
        name2 = " ".join(sorted(name2.split()))
    try:
        return round(fuzz.ratio(name1, name2) / 100, 2)
    except Exception as e:
        logger.warning(f"Similarity comparison failed: {e}")
        return None