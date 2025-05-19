from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime
from bson import ObjectId

from app.database import users_collection
from app.models.user import User, UserCreate
from app.auth.auth import (
    authenticate_user, 
    get_password_hash,
    generate_api_key
)

router = APIRouter(tags=["authentication"])

@router.post("/register", response_model=User)
async def register(user: UserCreate):
    if users_collection.find_one({"email": user.email}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email exists already."
        )
    
    hashed_password = get_password_hash(user.password)
    user_data = {
        "email": user.email,
        "hashed_password": hashed_password,
        "created_at": datetime.utcnow()
    }
    
    try:
        result = users_collection.insert_one(user_data)
        
        return {
            "id": str(result.inserted_id),
            "email": user.email,
            "created_at": user_data["created_at"]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    email = form_data.username
    
    user = authenticate_user(email, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    api_key = generate_api_key(user)
    
    return {"api_key": api_key, "user_id": str(user["_id"]), "email": user["email"]}

@router.post("/logout")
async def logout():
    return {"message": "Successfully logged out"}