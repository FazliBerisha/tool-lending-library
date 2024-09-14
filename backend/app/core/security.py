"""
Security Utilities.
- Provides functions for securely hashing and verifying passwords
- Can be expanded to include additional security-related operations in the future
"""

from passlib.context import CryptContext

# Initialize the password hashing context using the bcrypt algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """
    Hashes a plain text password using the bcrypt algorithm.
    
    Args:
        password (str): The plain text password to be hashed.
    
    Returns:
        str: The securely hashed password.
    """
    return pwd_context.hash(password)
