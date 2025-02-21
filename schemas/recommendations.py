from typing import List
from models.recommendation import Recommendation
from pydantic import BaseModel


class QueryBody(BaseModel):
    query: str

    class Config:
        json_schema_extra = {
            "example": {
                "query": "skin_rash",
            }
        }

class PaginatedResponse(BaseModel):
    status_code: int
    response_type: str
    description: str
    data: List[Recommendation]
    total: int
    page: int
    size: int

class Response(BaseModel):
    status_code: int
    response_type: str
    description: str
    data: Recommendation
