from sqlalchemy.orm import Session
import json
from fastapi import HTTPException,status
from app.modules.user.user_model import UserModel
from itsdangerous import URLSafeTimedSerializer
from app.core.config import settings


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
        "order_items": user_data
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


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

