from fastapi import Body, APIRouter, HTTPException
from passlib.context import CryptContext

from auth.jwt_handler import sign_jwt
from database.database import add_admin
from models import User
from schemas.admin import AdminData, AdminSignIn

router = APIRouter()

hash_helper = CryptContext(schemes=["bcrypt"])


@router.post("/login")
async def admin_login(admin_credentials: AdminSignIn = Body(...)):
    admin_exists = await User.find_one(User.email == admin_credentials.username)
    print(admin_exists)
    if admin_exists:
        password = hash_helper.verify(admin_credentials.password, admin_exists.password)
        if password:
            return sign_jwt(admin_exists.id,admin_exists.email)

        raise HTTPException(status_code=403, detail="Incorrect email or password")

    raise HTTPException(status_code=403, detail="Incorrect email or password")


@router.post("/register")
async def admin_signup(admin: User = Body(...)):
    admin_exists = await User.find_one(User.email == admin.email)
    if admin_exists:
        raise HTTPException(
            status_code=409, detail="User with email supplied already exists"
        )

    admin.password = hash_helper.encrypt(admin.password)
    new_admin = await add_admin(admin)
    return sign_jwt(new_admin.id,new_admin.email)
