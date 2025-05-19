from fastapi import Depends, HTTPException, status, Header
from passlib.context import CryptContext
from typing import Optional
import base64

from app.database import users_collection

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user_by_email(email: str):
    user = users_collection.find_one({"email": email})
    if user:
        user["id"] = str(user["_id"])
        return user
    return None

def authenticate_user(email: str, password: str):
    user = get_user_by_email(email)
    if not user:
        return False
    if not verify_password(password, user["hashed_password"]):
        return False
    return user

async def get_api_key(api_key: Optional[str] = Header(None, alias="X-API-Key")):
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key is missing",
        )
    
    try:
        decoded = base64.b64decode(api_key).decode("utf-8")
        email, user_id = decoded.split(":")
        
        user = get_user_by_email(email)
        if not user or str(user["_id"]) != user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid API key",
            )
        
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key format",
        )

def generate_api_key(user):
    email = user["email"]
    user_id = str(user["_id"])
    api_key = base64.b64encode(f"{email}:{user_id}".encode("utf-8")).decode("utf-8")
    return api_key