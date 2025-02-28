from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.utils.auth import get_current_user
from typing import Optional
from app.modules.user.user_model import UserModel
from app.modules.user.user_service import get_all_users

router = APIRouter()

@router.get("/", status_code=status.HTTP_200_OK)
def get_all_users_endpoint(db: Session = Depends(get_db),current_user: UserModel = Depends(get_current_user)):
    
    users_data = get_all_users(db=db, current_user=current_user)
    return users_data