from sqlalchemy.orm import Session
import json
from fastapi import HTTPException,status
from app.modules.user.user_model import UserModel
from itsdangerous import URLSafeTimedSerializer
from app.core.config import settings
from app.modules.user.user_schema import CreateUseSchema, UpdateUserSchema, UpdateUserRoleSchema
from app.modules.role.role_model import RoleModel


def get_all_users(db: Session , current_user:UserModel):

    try:
        query = db.query(UserModel).filter(UserModel.is_deleted == False)

        user_data = query.all()

        if not user_data:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND ,
                detail = "No User found"
            )
        

        return {
        "message": "Users retrieved successfully",
        "total": len(user_data),
        "users": user_data
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


def get_user_by_id(db: Session, user_id: int, current_user: UserModel):
   
    getUser = db.query(UserModel).filter(UserModel.user_id == user_id, UserModel.is_deleted == False).first()

    if not getUser:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user_dict = {user.user_id: user.user_name for user in db.query(UserModel).all()}
    getUser.created_by_name = user_dict.get(getUser.created_by, 'Unknown')
    getUser.updated_by_name = user_dict.get(getUser.updated_by, 'Unknown')


    return {
        "message": "User retrieved successfully",
        "role": getUser
    }


def create_user(db: Session, user_service_data: CreateUseSchema, current_user: UserModel):
    
    try:

        user_dict = user_service_data.dict(exclude_unset=True)
        user_dict["created_by"] = current_user.user_id
        new_user = UserModel(**user_dict)
    
    # Add the new order_item to the database session and commit the changes
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        # Return the newly created order_item
        return {
            "message": "user created successfully",
            "role": new_user
        }
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating user: {str(e)}")


def update_user(
    db: Session, user_id: int, user_service_data: UpdateUserSchema, current_user: UserModel
):
    try:
        # Fetch existing order item
        get_update_user = db.query(UserModel).filter(
            UserModel.user_id == user_id, UserModel.is_deleted == False
        ).first()

        if not get_update_user:
            raise HTTPException(status_code=404, detail="User not found")


        # Convert schema to dictionary and update only provided fields
        update_data = user_service_data.dict(exclude_unset=True)
        update_data["updated_by"] = current_user.user_id

        for key, value in update_data.items():
        #     if key == 'dimention_type' and value:
        #         value = DimentionTypeEnum(value)
            setattr(get_update_user, key, value)

        # Commit changes to the database
        db.commit()
        db.refresh(get_update_user)

        return {
        "message": "User updated successfully",
        "role": get_update_user
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Error updating user: {str(e)}")


def delete_existing_user(db: Session, user_id: int, current_user: UserModel):
   
    deleted_user = db.query(UserModel).filter(UserModel.user_id == user_id, UserModel.is_deleted == False).first()
    
    if not deleted_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found or already deleted"
            )
        
    deleted_user.is_deleted = True 
    deleted_user.is_active = False
    db.commit()  
    db.refresh(deleted_user) 
    
    return deleted_user


def update_user_role(db: Session, user_id: int, update_user_role_data:UpdateUserRoleSchema,  current_user: UserModel):

    get_user = db.query(UserModel).filter(UserModel.user_id == user_id, UserModel.is_deleted == False).first()
    get_role = db.query(RoleModel).all()

    if not get_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
            )

    if not get_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Role not found"
        )

    get_user.role_id = update_user_role_data.role_id
    db.commit()
    db.refresh(get_user)

    return {"message": "User role updated successfully",
            "user_role" : get_user}
    



class PasswordResetTokenGenerator:
    def __init__(self):
        self.serializer = URLSafeTimedSerializer(settings.jwt_secret_key)

    def make_token(self, user_id: int) -> str:
        """
        Generate a password reset token.
        """
        return self.serializer.dumps(user_id, salt="password-reset")
    
    def confirm_token(self, token: str, expiration: int = 3600) -> int:
        """
        Confirm and decode the token. Raise an exception if invalid or expired.
        """
        try:
            # The `max_age` argument should be passed here to enforce token expiration
            user_id = self.serializer.loads(token, salt="password-reset", max_age=expiration)
            print(f"Decoded User ID: {user_id}")
        except Exception as e:
            print(f"Token Validation Error: {e}")
            raise ValueError("Invalid or expired token")
        return user_id

