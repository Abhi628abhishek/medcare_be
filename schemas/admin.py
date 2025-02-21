from pydantic import BaseModel
from fastapi.security import HTTPBasicCredentials
from pydantic import EmailStr

class AdminSignIn(HTTPBasicCredentials):
    class Config:
        json_schema_extra = {
            "example": {"username": "abdul@youngest.dev", "password": "3xt3m#"}
        }


class AdminData(BaseModel):
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
                "email": "abdul@youngest.dev",
            }
        }
