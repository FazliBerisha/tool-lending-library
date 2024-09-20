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

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies if the plain text password matches the hashed password.
    
    Args:
        plain_password (str): The plain text password to verify.
        hashed_password (str): The previously hashed password to compare against.
    
    Returns:
        bool: True if the passwords match, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)

