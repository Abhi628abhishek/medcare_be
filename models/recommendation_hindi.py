from datetime import datetime
from typing import Optional, Any

from beanie import Document, Link
from pydantic import BaseModel, EmailStr

from models import User


class RecommendationHindi(Document):
    disease: str
    description: str
    precaution: list
    medications: list
    workouts: list
    diets: list
    symptoms: list
    user: Link[User]
    created_at: datetime = datetime.utcnow()

    class Config:
        json_schema_extra = {
        }

    class Settings:
        name = "recommendation_hindi"
