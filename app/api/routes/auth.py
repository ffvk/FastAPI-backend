from fastapi import APIRouter, Depends, HTTPException,Form
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.modules.user.user_model import UserModel
from app.utils.jwt import create_access_token
from app.utils.password import verify_password
from datetime import timedelta,datetime
from app.utils.email import send_email, render_email_template
from app.utils.password import hash_password, verify_password, validate_password
from app.core.config import settings
from app.utils.jwt import create_access_token
from app.utils.auth import get_current_user
from app.modules.user.auth_service import PasswordResetTokenGenerator
# from app.modules.role.role_model import RoleModel
from app.modules.user.user_schema import CreateUseSchema, DeleteUserSchema
from app.modules.user.auth_service import register_user, verify_email, send_verification_email







router = APIRouter()


@router.post("/login", status_code=200)
def login( email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
   
    # Retrieve user from the database by email
    user = db.query(UserModel).filter(UserModel.email == email).first()
    # Check if the user exists and if the password is valid
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create an access token
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=settings.jwt_access_token_expire_minutes)
    )
    # Return the access token and token type
    return {"access_token": access_token, "token_type": "bearer"}


@router.put("/update-password", status_code=200)
def update_password(
    old_password: str, 
    new_password: str, 
    current_user: UserModel = Depends(get_current_user), 
    db: Session = Depends(get_db)
    ):
    
    # Check if the old password is correct
    if not verify_password(old_password, current_user.password_hash):
        raise HTTPException(status_code=400, detail="Old password is incorrect.")
    
    # Check if the new password is the same as the old password
    if old_password == new_password:
        raise HTTPException(status_code=400, detail="New password must be different from the old password.")
    
    # Validate the new password strength
    if not validate_password(new_password):
        raise HTTPException(
            status_code=400,
            detail="Password must be at least 8 characters long, contain an uppercase letter, a special character, and a number."
        )
    
    # Hash the new password and update it in the database
    hashed_password = hash_password(new_password)
    current_user.password_hash = hashed_password
    db.commit()
    return {"msg": "Password updated successfully"}



@router.post("/forgot-password", status_code=200)
def forgot_password(email: str = Form(...), db: Session = Depends(get_db)):
   
    # Check if user with the provided email exists
    user = db.query(UserModel).filter(UserModel.email == email).first()
    if not user:
        # If no user is found, raise an HTTP error
        raise HTTPException(status_code=404, detail="User not found")
    
    # Initialize token generator to create a reset token
    token_generator = PasswordResetTokenGenerator()
    reset_token = token_generator.make_token(user.user_id)
    
    # Use settings for domain URL
    domain_url = settings.domain_url 
    
    # Create the password reset link with the token embedded
    reset_link = f"{domain_url}/reset-password?token={reset_token}"
    
    # Prepare context for the email template
    context = {
        'reset_url': reset_link
    }

    # Render the email body from the template
    email_body = render_email_template('password_reset_email.html', context)
    
    # Send the reset link to the user's email address
    send_email(to_email=email, subject="Reset Your Password", body=email_body)
    
    # Return a success message to the client
    return {"message": "Password reset link sent to your email"}


@router.post("/reset-password", status_code=200)
def reset_password(token: str = Form(...), new_password: str = Form(...), db: Session = Depends(get_db)):
   
    # Initialize token generator to confirm the reset token
    token_generator = PasswordResetTokenGenerator()
    
    try:
        # Decode and validate the token, returning the user ID
        user_id = token_generator.confirm_token(token)
    except ValueError as e:
        # If the token is invalid or expired, raise an error
        raise HTTPException(status_code=400, detail=str(e))
    
    # Find the user by the decoded user ID
    user = db.query(UserModel).filter(UserModel.user_id == user_id).first()
    if not user:
        # If no user is found, raise an HTTP error
        raise HTTPException(status_code=404, detail="User not found")
    
    # Find the user by the decoded user ID
    user = db.query(UserModel).filter(UserModel.user_id == user_id).first()
    if not user:
        # If no user is found, raise an HTTP error
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if the new password is strong enough using the validate_password function
    if not validate_password(new_password):
        raise HTTPException(
            status_code=400,
            detail="Password must be at least 8 characters long, contain an uppercase letter, a special character, and a number."
        )
    
    # Hash the new password and update it in the database
    user.password_hash = hash_password(new_password)
    
    # Commit the changes to the database
    db.commit()
    
    # Return a success message indicating password reset
    return {"message": "Password reset successful"}


@router.post("/register", response_model=DeleteUserSchema)
async def register_user_endpoint(user_data: CreateUseSchema, db: Session = Depends(get_db)):
    
    await register_user(db=db, register_user_data=user_data)
    
    return {"message" : "Register successfully",}


@router.get("/verify-email", response_model=DeleteUserSchema)
def verify_email_endpoint(token: str, db: Session = Depends(get_db)):

    verify_email(token=token, db=db )

    return {"message": "Email verified successfully!"}



@router.post("/send-verification-email", response_model=DeleteUserSchema)
async  def send_verification_email_endpoint(email: str, token: str):
    await send_verification_email(email=email, token=token )
    return {"message": "Email successfully send"}