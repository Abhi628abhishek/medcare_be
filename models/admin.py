from beanie import Document
from fastapi.security import HTTPBasicCredentials
from pydantic import BaseModel, EmailStr


class User(Document):
    name: str
    gender: str
    dob: str
    email: EmailStr
    password: str
    is_admin: bool = False
    phone: int

    class Config:
        json_schema_extra = {
            "example": {
                "fullname": "Admin MedCare",
                "email": "admin.medcare@yopmail.com",
                "password": "Admin@123",
            }
        }

    class Settings:
        name = "user"


class AdminSignIn(HTTPBasicCredentials):
    is_admin: bool
    class Config:
        json_schema_extra = {
            "example": {"username": "admin.medcare@yopmail.com", "password": "Admin@123"}
        }


class AdminData(BaseModel):
    fullname: str
    email: EmailStr

    class Config:
        json_schema_extra = {
            "example": {
                "fullname": "Admin MedCare",
                "email": "admin.medcare@yopmail.com",
            }
        }
