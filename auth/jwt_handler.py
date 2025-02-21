import time
from typing import Dict

import jwt
from beanie import PydanticObjectId
from pydantic import EmailStr
from config.config import Settings


def token_response(token: str):
    return {"access_token": token}


secret_key = Settings().secret_key


def sign_jwt(user_id: PydanticObjectId,email: EmailStr) -> Dict[str, str]:
    # Set the expiry time.
    user_id = str(user_id)
    payload = {"user_id": user_id,"email":email,"expires": time.time() + 2400}
    return token_response(jwt.encode(payload, secret_key, algorithm="HS256"))


def decode_jwt(token: str) -> dict:
    decoded_token = jwt.decode(token.encode(), secret_key, algorithms=["HS256"])
    return decoded_token if decoded_token["expires"] >= time.time() else {}
