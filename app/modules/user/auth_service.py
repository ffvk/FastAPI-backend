from itsdangerous import URLSafeTimedSerializer
from app.core.config import settings
from sqlalchemy.orm import Session
from app.modules.user.user_model import UserModel
from app.modules.role.role_model import RoleModel
from app.modules.user.user_schema import CreateUseSchema
from fastapi import  HTTPException
from datetime import datetime, timedelta
from app.utils.password import hash_password
from app.utils.jwt import verify_access_token, create_access_token
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from app.core.mail_config import conf



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



async def send_verification_email(email: str, token: str):
    """Send a verification email with a JWT token."""
    verification_url = f"http://localhost:8000/verify-email?token={token}"
    message = MessageSchema(
        subject="Verify Your Email",
        recipients=[email],
        body=f"Click <a href='{verification_url}'>here</a> to verify your email.",
        subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(message)



async def register_user(
    db: Session,
    register_user_data: CreateUseSchema
):
    try:
        existing_user = db.query(UserModel).filter(UserModel.email == register_user_data.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        

        # Fetch the role_id for "customer"
        customer_role = db.query(RoleModel).filter(RoleModel.role_name == "customer").first()
        if not customer_role:
            raise HTTPException(status_code=400, detail="Customer role not found")


        # Hash the password before storing
        hashed_password = hash_password(register_user_data.password_hash)

        # Create new user with is_active = False
        user_dict = register_user_data.dict(exclude_unset=True)
        user_dict["password_hash"] = hashed_password
        user_dict["role_id"] = customer_role.role_id
        user_dict["is_active"] = False  
        user_dict["created_at"] = datetime.utcnow()

        new_user = UserModel(**user_dict)

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        token = create_access_token({"email": new_user.email}, expires_delta=timedelta(hours=1))
        await send_verification_email(new_user.email, token)

        return new_user

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating register: {str(e)}")



def verify_email(token: str, db: Session):
    
    try:

        payload = verify_access_token(token)
        
        if not payload:
            raise HTTPException(status_code=400, detail="Invalid or expired token")
        
        email = payload.get("email")
        user = db.query(UserModel).filter(UserModel.email == email).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if user.is_active:
            return {"message": "Email is already verified."}

        # Activate the user
        user.is_active = True
        db.commit()

        # return user

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating verify email: {str(e)}")     


