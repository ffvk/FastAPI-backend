from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class GetRoleSchema(BaseModel):
    role_id: Optional[int]
    role_name: Optional[str]
    is_active: Optional[bool]
    is_deleted: Optional[bool]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    created_by_name: Optional[str]
    updated_by_name: Optional[str]
    created_by: Optional[int]
    updated_by: Optional[int]
    order_id: Optional[int]

class CreateRoleSchema(BaseModel):
    role_name: Optional[str]
    is_active: Optional[bool] = True

class UpdateRoleSchema(BaseModel):
    role_name: Optional[str]
    is_active: Optional[bool]
    

class DeleteRoleSchema(BaseModel):
    message : str

class Config:
    orm_mode = True
