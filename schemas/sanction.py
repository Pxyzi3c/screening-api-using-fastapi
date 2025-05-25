from typing import Optional
from pydantic import BaseModel

class SanctionSchema(BaseModel):
    ent_num: int
    sdn_name: str
    sdn_type: str
    complete_address: str
    country: str
    add_remarks: str
    cleaned_name: str
    similarity_score: Optional[float]