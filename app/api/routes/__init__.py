from fastapi import APIRouter
from app.api.routes import auth
from app.modules.role import role_router
from app.modules.user import user_router




routes = APIRouter()


routes.include_router(auth.router, prefix="/auth", tags=["Auth"])
routes.include_router(role_router.router, prefix="/roles", tags=["Roles"])
routes.include_router(user_router.router, prefix="/users", tags=["Users"])
