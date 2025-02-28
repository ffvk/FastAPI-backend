from pydantic_settings import BaseSettings
from pathlib import Path

# Get the absolute path of the .env file
BASE_DIR = Path(__file__).resolve().parent.parent  # Points to the root directory
ENV_FILE = BASE_DIR / ".env"

class Settings(BaseSettings):
    app_name: str
    database_url: str
    jwt_secret_key: str
    jwt_algorithm: str
    jwt_access_token_expire_minutes: int
    email_host_user: str 
    email_host_password: str 
    domain_url: str
    email_smtp_server: str
    email_smtp_port: int


    class Config:
        env_file = str(ENV_FILE)       # Specify the path to your .env file
        extra = "allow"

# Create an instance of Settings to access environment variables
settings = Settings()
