from sqlalchemy.orm import Session
import json
from fastapi import HTTPException,status
from app.modules.user.user_model import UserModel
from app.modules.role.role_model import RoleModel


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
        "order_items": role_data
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))