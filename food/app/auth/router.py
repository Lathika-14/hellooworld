from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    ChangePasswordRequest,
)

from app.auth.service import (
    register_user,
    login_user,
    change_password,
)

from app.auth.dependencies import get_current_user

from app.models.user import User

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register", status_code=201)
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db),
):
    return register_user(db, request)


@router.post("/login")
def login(
    request: LoginRequest,
    db: Session = Depends(get_db),
):
    return login_user(db, request)


@router.get("/me")
def get_me(
    current_user: User = Depends(get_current_user),
):
    return {
        "user_id": current_user.user_id,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "email": current_user.email,
        "phone": current_user.phone,
        "role": current_user.role.role_name,
    }


@router.patch("/change-password")
def change_user_password(
    request: ChangePasswordRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return change_password(
        db,
        current_user,
        request,
    )