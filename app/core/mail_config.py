from fastapi_mail import ConnectionConfig, FastMail, MessageSchema
from pydantic_settings import BaseSettings
import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent  # Points to the root directory
ENV_FILE = BASE_DIR / ".env"

class MailConfig(BaseSettings):
    EMAIL_HOST_USER: str
    EMAIL_HOST_PASSWORD: str
    EMAIL_FROM: str
    EMAIL_SMTP_SERVER: str
    EMAIL_SMTP_PORT: int = 587
    EMAIL_STARTTLS: bool = True
    EMAIL_SSL_TLS: bool = False
    USE_CREDENTIALS: bool = True

    class Config:
        env_file = str(ENV_FILE)       # Specify the path to your .env file
        extra = "allow"


# # Load settings from .env file
mail_settings = MailConfig()

# Configure FastAPI-Mail
conf = ConnectionConfig(
    MAIL_USERNAME=mail_settings.EMAIL_HOST_USER,
    MAIL_PASSWORD=mail_settings.EMAIL_HOST_PASSWORD,
    MAIL_FROM=mail_settings.EMAIL_FROM,
    MAIL_SERVER=mail_settings.EMAIL_SMTP_SERVER,
    MAIL_PORT=mail_settings.EMAIL_SMTP_PORT,
    MAIL_STARTTLS=mail_settings.EMAIL_STARTTLS,  # Corrected field
    MAIL_SSL_TLS=mail_settings.EMAIL_SSL_TLS,    # Corrected field
    USE_CREDENTIALS=mail_settings.USE_CREDENTIALS
)
