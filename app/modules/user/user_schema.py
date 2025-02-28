from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from fastapi import HTTPException, status
from sqlalchemy.orm import Session


class GetUserSchema(BaseModel):
    user_id: Optional[int]
    user_name: Optional[str]
    email: Optional[str]
    password_hash: Optional[str]
    phone_number: Optional[int]

    is_active: Optional[bool]
    is_deleted: Optional[bool]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    created_by_name: Optional[str]
    updated_by_name: Optional[str]
    created_by: Optional[int]
    updated_by: Optional[int]

    role_id: Optional[int]
    


class CreateUseSchema(BaseModel):
    user_name: Optional[str]
    email: Optional[str]
    password_hash: Optional[str]
    phone_number: Optional[int]
    is_active: Optional[bool] = True

    role_id : Optional[int]


class UpdateUserSchema(BaseModel):
    user_name: Optional[str]
    email: Optional[str]
    password_hash: Optional[str]
    phone_number: Optional[int]
    is_active: Optional[bool]

    role_id : Optional[int]
    

class DeleteUserSchema(BaseModel):
    message : str

class Config:
    orm_mode = True
    from_attributes = True