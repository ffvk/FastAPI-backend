from sqlalchemy import Column, Integer, String, Boolean, DateTime,ForeignKey
from datetime import datetime
from app.db.base import Base
from sqlalchemy.orm import relationship


class UserModel(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    user_name = Column(String(255), nullable=False)
    phone_number = Column(String(20), nullable=True)

    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(Integer)
    updated_by = Column(Integer)

    role_id = Column(Integer, ForeignKey("roles.role_id"))


    # roles = relationship("Role", backref="users_with_role", foreign_keys=[role_id])
    roles = relationship("RoleModel", back_populates="users")

