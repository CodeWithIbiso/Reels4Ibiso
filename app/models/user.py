from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    hashed_password: str

class UserResponse(UserBase):
    id: Optional[str]