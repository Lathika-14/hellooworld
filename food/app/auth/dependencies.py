from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.repositories.user_repository import get_user_by_id
from app.auth.jwt_handler import verify_access_token


# Swagger Authorize button
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    """
    Get the currently logged-in user from JWT token.
    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = verify_access_token(token)

        user_id = payload.get("user_id")

        if user_id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = get_user_by_id(db, user_id)

    if user is None:
        raise credentials_exception

    return user


def require_roles(allowed_roles: list):
    """
    Restrict endpoint access based on role.
    """

    def role_checker(
        current_user: User = Depends(get_current_user),
    ):
        if current_user.role.role_name not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not authorized to perform this action.",
            )

        return current_user

    return role_checker


# -------- Individual Role Dependencies -------- #

def require_super_admin():
    return require_roles(["SUPER_ADMIN"])


def require_restaurant_admin():
    return require_roles(["RESTAURANT_ADMIN"])


def require_delivery_agent():
    return require_roles(["DELIVERY_AGENT"])


def require_customer():
    return require_roles(["CUSTOMER"])