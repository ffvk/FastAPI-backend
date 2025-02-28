import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from fastapi import HTTPException
from app.core.config import settings
from jinja2 import Environment, FileSystemLoader
from itsdangerous import URLSafeTimedSerializer

# Configure the secret key and salt for token generation
serializer = URLSafeTimedSerializer(settings.jwt_secret_key)

# Jinja2 setup
template_env = Environment(
    loader=FileSystemLoader('app/templates'),
    autoescape=True
)

def render_email_template(template_name: str, context: dict) -> str:
    """
    Renders an email template with the provided context.
    """
    template = template_env.get_template(template_name)
    return template.render(context)

def send_email(to_email: str, subject: str, body: str):
    try:
        # Connect to the SMTP server
        server = smtplib.SMTP(settings.email_smtp_server, settings.email_smtp_port)
        server.starttls()
        server.login(settings.email_host_user, settings.email_host_password)

        # Create the email message
        msg = MIMEMultipart()
        msg['From'] = settings.email_host_user
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))

        # Send the email
        server.sendmail(settings.email_host_user, to_email, msg.as_string())
        server.quit()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Email sending failed: {str(e)}")

def send_welcome_email(to_email: str, first_name: str, last_name: str, password: str):
    subject = "Welcome to Our Service"
    context = {
        'first_name': first_name,
        'last_name': last_name,
        'email': to_email,
        'password': password
    }
    body = render_email_template('welcome_email.html', context)
    send_email(to_email, subject, body)

def send_password_reset_email(to_email: str, reset_token: str):
    reset_url = f"{settings.frontend_url}/reset-password/{reset_token}"
    subject = "Password Reset Request"
    context = {
        'reset_url': reset_url
    }
    body = render_email_template('password_reset_email.html', context)
    send_email(to_email, subject, body)
