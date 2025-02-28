from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.utils.auth import get_current_user
from typing import Optional
from app.modules.user.user_model import UserModel
from app.modules.user.user_schema import CreateUseSchema, UpdateUserSchema, DeleteUserSchema, UpdateUserRoleSchema
from app.modules.user.user_service import get_all_users, get_user_by_id, create_user, update_user, delete_existing_user, update_user_role

router = APIRouter()

@router.get("/", status_code=status.HTTP_200_OK)
def get_all_users_endpoint(db: Session = Depends(get_db),current_user: UserModel = Depends(get_current_user)):
    
    users_data = get_all_users(db=db, current_user=current_user)
    return users_data


@router.get("/{user_id}",status_code=status.HTTP_200_OK)
def get_user_by_id_endpoint (user_id:int, db:Session = Depends(get_db),current_user: UserModel = Depends(get_current_user)):

    get_user_data = get_user_by_id(db=db, user_id=user_id, current_user=current_user)

    return get_user_data


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_new_role_endpoint(
    newUser:CreateUseSchema,
    db: Session=Depends(get_db),
    current_user: UserModel= Depends(get_current_user)
    
    ):
   
    new_user = create_user(db=db,user_service_data=newUser,current_user=current_user)
        
    return new_user


@router.put("/{user_id}", status_code=status.HTTP_200_OK)
async def update_existing_user_endpoint(
    user_id: int,
    userUpdate: UpdateUserSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    updated_user = update_user(
        db=db, user_id=user_id, user_service_data=userUpdate, current_user=current_user
    )
    
    return updated_user


@router.delete("/{user_id}",  response_model= DeleteUserSchema)
def delete_user_endpoint(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
    ):
    """
    Soft delete a user by ID.
    """
   
    delete_existing_user(db=db, user_id=user_id, current_user=current_user)
    
    
    return {"message" : "User deleted successfully",}

@router.put("/user-role/{user_id}", status_code=status.HTTP_200_OK)
async def update_existing_user_role_endpoint(
    user_id: int,
    update_userRole: UpdateUserRoleSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    updated_userRole = update_user_role(
        db=db, user_id=user_id, update_user_role_data=update_userRole, current_user=current_user
    )
    
    return updated_userRole


