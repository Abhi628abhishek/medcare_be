from typing import Optional, Any

from beanie import Document
from pydantic import BaseModel, EmailStr


class User(Document):
    fullname: str
    email: EmailStr
    year: int
    password: str
    age: int

    class Config:
        json_schema_extra = {
            "example": {
                "fullname": "Admin MedCare",
                "email": "abdul@school.com",
                "course_of_study": "Water resources engineering",
                "year": 4,
                "gpa": "3.76",
            }
        }

    class Settings:
        name = "student"
