from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.user_service import UserService
from app.schemas.user import UserCreate, User, UserProfileUpdate
from app.core.auth import get_current_user_role, get_current_user
from app.services.file_service import FileService

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/token")

@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user with the provided details:
    - Checks if the email is already registered; raises an HTTP 400 error if it is.
    - Creates a new user if the email is unique.
    - Returns the created user data upon success.
    - Raises an HTTP 500 error for any unexpected issues during the process.
    """
    # Check if a user with the given email already exists in the database
    db_user = UserService.get_user_by_email(db, email=user.email)
    
    # If the email is already registered, return an HTTP 400 error
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    # If the email is unique, proceed to create a new user
    try:
        return UserService.create_user(
            db=db,              # Pass the database session
            username=user.username,  # Provide the username from the request body
            email=user.email,        # Provide the email from the request body
            password=user.password,  # Provide the password (should be hashed inside the service)
            role=user.role           # Provide the role (optional, depending on your system)
        )
    except Exception as e:
        # Handle any unexpected exceptions and return a 500 error with the exception message
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """
    Retrieve user details by user ID.
    - If the user is not found, raises an HTTP 404 error.
    - Returns the user data if found.
    """
    db_user = UserService.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user

@router.get("/admin/users", response_model=list[User])
async def list_all_users(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    Retrieve a list of all users in the system.
    This is an admin-only endpoint that requires authentication with an admin role.

    Args:
    - db (Session): The database session, automatically provided by FastAPI's dependency injection.
    - token (str): The JWT token for authentication, automatically extracted from the request headers.

    Returns:
    - list[User]: A list of all user objects in the system.

    Raises:
    - HTTPException (status_code=403): If the authenticated user is not an admin.
    - HTTPException (status_code=401): If the token is invalid or missing (raised by get_current_user_role).

    Note:
    This function first verifies the user's role using the provided token.
    If the user is not an admin, it raises a 403 Forbidden exception.
    If the user is an admin, it retrieves and returns all users from the database.
    """
    current_user_role = get_current_user_role(token)
    if current_user_role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return UserService.get_all_users(db)

@router.get("/profile/{user_id}", response_model=User)
def get_user_profile(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Retrieve a user's profile.
    
    Args:
        user_id (int): The ID of the user whose profile is being requested.
        db (Session): The database session.
        current_user (User): The currently authenticated user.

    Returns:
        User: The requested user's profile.

    Raises:
        HTTPException: 404 if user not found, 403 if unauthorized to view the profile.
    """
    profile = UserService.get_user_profile(db, user_id)
    if profile is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if current_user.id != user_id and current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this profile")
    return profile

@router.put("/profile/{user_id}", response_model=User)
def update_user_profile(
    user_id: int,
    profile_data: UserProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update a user's profile.
    
    Args:
        user_id (int): The ID of the user whose profile is being updated.
        profile_data (UserProfileUpdate): The new profile data.
        db (Session): The database session.
        current_user (User): The currently authenticated user.

    Returns:
        User: The updated user profile.

    Raises:
        HTTPException: 404 if user not found, 403 if unauthorized to update the profile.
    """
    user = UserService.get_user_profile(db, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if current_user.id != user_id and current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this profile")
    updated_profile = UserService.update_user_profile(db, user_id, profile_data)
    return updated_profile

@router.put("/profile-image")
async def update_profile_image(
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        # Save the uploaded image
        image_url = await FileService.save_upload(image, "profile-images")
        
        # Update user's profile image
        updated_user = UserService.update_profile_image(db, current_user.id, image_url)
        
        return {"message": "Profile image updated successfully", "image_url": image_url}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))