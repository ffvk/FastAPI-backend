from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.modules.user.user_model import UserModel
from app.utils.password import get_password_hash, verify_password
# from app.utils.jwt import create_access_token  # For JWT login

router = APIRouter()

# Default Superadmin Credentials
SUPERADMIN_EMAIL = "dhriti@ovntech.com"
SUPERADMIN_PASSWORD = "Admin@123"  # Set your own secure password

@router.post("/seed")
def seed_superadmin(db: Session = Depends(get_db)):
    """API to create a default Superadmin user if not exists"""
    existing_user = db.query(UserModel).filter(UserModel.email == SUPERADMIN_EMAIL).first()

    if existing_user:
        return {"message": "Superadmin already exists"}

    hashed_password = get_password_hash(SUPERADMIN_PASSWORD)
    superadmin = UserModel(
        user_name="superadmin",
        email=SUPERADMIN_EMAIL,
        password_hash=hashed_password,
        role_id=1
    )

    db.add(superadmin)
    db.commit()
    db.refresh(superadmin)

    return {"message": "Superadmin created successfully", "email": superadmin.email}
