from passlib.context import CryptContext
import re
import random
import string

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def validate_password(password: str) -> bool:
    """
    Validates that the password is at least 8 characters long, contains
    uppercase, lowercase, numbers, and special characters.
    """
    if len(password) < 8:
        return False
    if not re.search(r'[A-Z]', password):  # Check for uppercase letter
        return False
    if not re.search(r'[a-z]', password):  # Check for lowercase letter
        return False
    if not re.search(r'[0-9]', password):  # Check for digit
        return False
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):  # Check for special character
        return False
    return True


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def generate_strong_password(length: int = 12) -> str:
    if length < 12:
        raise ValueError("Password length must be at least 12 characters")
    uppercase = string.ascii_uppercase
    lowercase = string.ascii_lowercase
    digits = string.digits
    special = "!@#$%^&*()-_+="
    password = [
        random.choice(uppercase),
        random.choice(lowercase),
        random.choice(digits),
        random.choice(special),
    ]
    all_characters = uppercase + lowercase + digits + special
    password += random.choices(all_characters, k=length - len(password))
    random.shuffle(password)
    return "".join(password)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


