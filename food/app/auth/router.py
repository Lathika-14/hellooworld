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

from app.auth.dependencies import (
    get_current_user,
    require_super_admin,
    require_restaurant_admin,
    require_delivery_agent,
    require_customer,
)

from app.models.user import User

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# ---------------------- Register ---------------------- #

@router.post("/register", status_code=201)
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db),
):
    return register_user(db, request)


# ---------------------- Login ---------------------- #

@router.post("/login")
def login(
    request: LoginRequest,
    db: Session = Depends(get_db),
):
    return login_user(db, request)


# ---------------------- Current User ---------------------- #

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


# ---------------------- Change Password ---------------------- #

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


# ==========================================================
# TEMPORARY AUTHORIZATION TEST ENDPOINTS
# (Remove these after testing)
# ==========================================================

# ---------------------- Super Admin ---------------------- #

@router.get("/admin-dashboard")
def admin_dashboard(
    current_user: User = Depends(require_super_admin()),
):
    return {
        "message": "Welcome Super Admin",
        "email": current_user.email,
        "role": current_user.role.role_name,
    }


# ---------------------- Restaurant Admin ---------------------- #

@router.get("/restaurant-dashboard")
def restaurant_dashboard(
    current_user: User = Depends(require_restaurant_admin()),
):
    return {
        "message": "Welcome Restaurant Admin",
        "email": current_user.email,
        "role": current_user.role.role_name,
    }


# ---------------------- Delivery Agent ---------------------- #

@router.get("/delivery-dashboard")
def delivery_dashboard(
    current_user: User = Depends(require_delivery_agent()),
):
    return {
        "message": "Welcome Delivery Agent",
        "email": current_user.email,
        "role": current_user.role.role_name,
    }


# ---------------------- Customer ---------------------- #

@router.get("/customer-dashboard")
def customer_dashboard(
    current_user: User = Depends(require_customer()),
):
    return {
        "message": "Welcome Customer",
        "email": current_user.email,
        "role": current_user.role.role_name,
    }