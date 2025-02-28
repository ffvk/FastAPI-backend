from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.security import OAuth2PasswordBearer
from app.api.routes import routes
from app.core.config import settings
# from app.modules.user.user_schema import UpdateUserSchema
# from app.utils.globle_status import create_default_status
from app.db.session import get_db
from fastapi.middleware.cors import CORSMiddleware

# Define the OAuth2 scheme for JWT
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

app = FastAPI(title="FastAPI MySQL App")

@app.on_event("startup")
async def on_startup():
    db = next(get_db())
    # create_default_status(db)

# Include routers
app.include_router(routes)

# Add a root endpoint
@app.get("/")
def read_root():
    return settings.app_name

# CORS Middleware configuration
origins = [
    "http://localhost:5173",  # Your frontend URL
    "http://127.0.0.1:5173", # Alternative frontend URL
    "http://209.105.242.30:7778", # live frontend URL
    "https://demo.avirise.in"

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Customize the OpenAPI schema to include JWT authorization
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="FastAPI MySQL App",
        version="1.0.0",
        description="API documentation for Logistic Application",
        routes=app.routes,
    )

    # Add security schemes (JWT)
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    # Apply security to all routes
    for path in openapi_schema["paths"].values():
        for operation in path.values():
            operation["security"] = [{"BearerAuth": []}]
    
    # Ensure the email field isn't clickable if empty in UpdateUserSchema schema
    try:
        user_update_schema = openapi_schema["components"]["schemas"]["UpdateUserSchema"]["properties"]
        if "email" in user_update_schema:
            user_update_schema["email"]["default"] = None
            user_update_schema["email"].pop("nullable", None)
    except KeyError:
        pass  # Handle case if "UpdateUserSchema" schema is not found
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


# Assign the custom OpenAPI schema
app.openapi = custom_openapi