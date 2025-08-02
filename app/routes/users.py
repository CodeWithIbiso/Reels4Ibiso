from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from models.user import UserCreate, UserResponse
from utils.auth import get_password_hash, verify_password, create_access_token
from connections.database import database
from datetime import timedelta
from bson import ObjectId
from typing import Dict
import re

router = APIRouter()
users_collection = database.get_collection("users")
active_tokens: Dict[str, str] = {}

def is_password_strong(password: str) -> bool:
    return bool(re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$', password))

@router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate):
    if not is_password_strong(user.password):
        raise HTTPException(status_code=400, detail="Password is not strong enough.")

    user_dict = user.dict()
    user_dict["hashed_password"] = get_password_hash(user_dict.pop("password"))
    try:
        result = await users_collection.insert_one(user_dict)
    except Exception as e:
        raise HTTPException(status_code=400, detail="User registration failed.")

    user_dict["id"] = str(result.inserted_id)
    return user_dict

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: str, user: UserCreate):
    user_dict = user.dict()
    user_dict["hashed_password"] = get_password_hash(user_dict.pop("password"))
    result = await users_collection.update_one(
        {"_id": ObjectId(user_id)}, {"$set": user_dict}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    user_dict["id"] = user_id
    return user_dict

@router.delete("/{user_id}")
async def delete_user(user_id: str):
    result = await users_collection.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted successfully"}

@router.post("/login")
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await users_collection.find_one({"email": form_data.username})
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )
    active_tokens[access_token] = user["email"]
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout")
async def logout_user(token: str):
    if token in active_tokens:
        del active_tokens[token]
        return {"detail": "Successfully logged out"}
    raise HTTPException(status_code=400, detail="Invalid token or already logged out")