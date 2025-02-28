from sqlalchemy.orm import Session
import json
from fastapi import HTTPException,status
from app.modules.user.user_model import UserModel
from app.modules.role.role_model import RoleModel
from app.modules.role.role_schema import CreateRoleSchema, UpdateRoleSchema


def get_all_roles(db: Session , current_user:UserModel):

    try:
        query = db.query(RoleModel).filter(RoleModel.is_deleted == False)

        role_data = query.all()

        if not role_data:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND ,
                detail = "No Role found"
            )
        

        return {
        "message": "Roles retrieved successfully",
        "total": len(role_data),
        "roles": role_data
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

def get_role_by_id(db: Session, role_id: int, current_user: UserModel):
   
    get_role = db.query(RoleModel).filter(RoleModel.role_id == role_id, RoleModel.is_deleted == False).first()

    if not get_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found"
        )
    
    user_dict = {user.user_id: user.user_name for user in db.query(UserModel).all()}
    get_role.created_by_name = user_dict.get(get_role.created_by, 'Unknown')
    get_role.updated_by_name = user_dict.get(get_role.updated_by, 'Unknown')


    return {
        "message": "Role retrieved successfully",
        "role": get_role
    }


def create_role(db: Session, role_service_data: CreateRoleSchema, current_user: UserModel):
    
    try:

        role_dict = role_service_data.dict(exclude_unset=True)
        role_dict["created_by"] = current_user.user_id
        new_role = RoleModel(**role_dict)
    
    # Add the new order_item to the database session and commit the changes
        db.add(new_role)
        db.commit()
        db.refresh(new_role)
        
        # Return the newly created order_item
        return {
            "message": "Role created successfully",
            "role": new_role
        }
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating role: {str(e)}")



def update_role(
    db: Session, role_id: int, role_service_data: UpdateRoleSchema, current_user: UserModel
):
    try:
        # Fetch existing order item
        get_update_role = db.query(RoleModel).filter(
            RoleModel.role_id == role_id, RoleModel.is_deleted == False
        ).first()

        if not get_update_role:
            raise HTTPException(status_code=404, detail="Role not found")


        # Convert schema to dictionary and update only provided fields
        update_data = role_service_data.dict(exclude_unset=True)
        update_data["updated_by"] = current_user.user_id

        for key, value in update_data.items():
        #     if key == 'dimention_type' and value:
        #         value = DimentionTypeEnum(value)
            setattr(get_update_role, key, value)

        # Commit changes to the database
        db.commit()
        db.refresh(get_update_role)

        return {
        "message": "Role updated successfully",
        "role": get_update_role
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Error updating role: {str(e)}")


def delete_existing_role(db: Session, role_id: int, current_user: UserModel):
   
    deleted_role = db.query(RoleModel).filter(RoleModel.role_id == role_id, RoleModel.is_deleted == False).first()
    
    if not deleted_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Role not found or already deleted"
            )
        
    
    
    deleted_role.is_deleted = True  # Mark as deleted (soft delete)
    deleted_role.is_active = False
    db.commit()  # Commit the changes
    db.refresh(deleted_role)  # Refresh to update the state
    
    return deleted_role
