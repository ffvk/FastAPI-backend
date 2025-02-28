from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.utils.auth import get_current_user
from app.modules.user.user_model import UserModel
from app.modules.role.role_schema import CreateRoleSchema, UpdateRoleSchema, DeleteRoleSchema
from app.modules.role.role_service import get_all_roles,get_role_by_id, create_role, update_role, delete_existing_role

router = APIRouter()

@router.get("/", status_code=status.HTTP_200_OK)
def get_all_roles_endpoint(db: Session = Depends(get_db),current_user: UserModel = Depends(get_current_user)):
    
    roles_data = get_all_roles(db=db, current_user=current_user)
    return roles_data


@router.get("/{role_id}",status_code=status.HTTP_200_OK)
def get_role_by_id_endpoint (role_id:int, db:Session = Depends(get_db),current_user: UserModel = Depends(get_current_user)):

    get_role_data = get_role_by_id(db=db, role_id=role_id,current_user=current_user)

    return get_role_data


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_new_role_endpoint(
    newRole:CreateRoleSchema,
    db: Session=Depends(get_db),
    current_user: UserModel= Depends(get_current_user)
    
    ):
   
    new_role = create_role(db=db,role_service_data=newRole,current_user=current_user)
        
    return new_role


@router.put("/{role_id}", status_code=status.HTTP_200_OK)
async def update_existing_role_endpoint(
    role_id: int,
    role_update: UpdateRoleSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    updated_role = update_role(
        db=db, role_id=role_id, role_service_data=role_update, current_user=current_user
    )
    
    return updated_role


@router.delete("/{role_id}",  response_model= DeleteRoleSchema)
def delete_role_endpoint(
    role_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
    ):
    """
    Soft delete a role by ID.
    """
   
    delete_existing_role(db=db, role_id=role_id, current_user=current_user)
    
    
    return {"message" : "Role deleted successfully",}

