from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.auth.jwt_handler import create_access_token
from app.auth.password import hash_password, verify_password

from app.models.user import User

from app.repositories.user_repository import (
    create_user,
    get_user_by_email,
    update_password,
    get_role_by_name,
)

from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    ChangePasswordRequest,
)
def register_user(db: Session, request: RegisterRequest):
    """
    Register a new customer.
    """

    # Check whether email already exists
    existing_user = get_user_by_email(db, request.email)

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Fetch CUSTOMER role
    customer_role = get_role_by_name(db, "CUSTOMER")

    if customer_role is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Customer role not found"
        )

    # Hash password
    hashed_password = hash_password(request.password)

    # Create User object
    new_user = User(
        first_name=request.first_name,
        last_name=request.last_name,
        email=request.email,
        password_hash=hashed_password,
        phone=request.phone,
        role_id=customer_role.role_id
    )

    # Save user
    user = create_user(db, new_user)

    return {
        "message": "Registration successful",
        "user_id": user.user_id,
        "email": user.email
    }

def login_user(db: Session, request: LoginRequest):
    """
    Login for all users.
    """

    # Find user
    user = get_user_by_email(db, request.email)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Verify password
    if not verify_password(request.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Generate JWT
    token = create_access_token(
        data={
            "user_id": user.user_id,
            "email": user.email,
            "role": user.role.role_name
        }
    )

    return {
        "message": "Login successful",
        "access_token": token,
        "token_type": "bearer"
    }

def change_password(
    db: Session,
    current_user: User,
    request: ChangePasswordRequest,
):
    """
    Change password.
    """

    # Verify current password
    if not verify_password(
        request.current_password,
        current_user.password_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )

    # Hash new password
    new_password_hash = hash_password(request.new_password)

    # Update password
    update_password(
        db,
        current_user,
        new_password_hash,
    )

    return {
        "message": "Password changed successfully"
    }