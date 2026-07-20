from sqlalchemy.orm import Session

from app.models.user import User
from app.models.role import Role


def get_user_by_email(db: Session, email: str):
    """
    Fetch a user by email.
    """
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int):
    """
    Fetch a user by user_id.
    """
    return db.query(User).filter(User.user_id == user_id).first()


def create_user(db: Session, user: User):
    """
    Create a new user.
    """
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_password(db: Session, user: User, new_password_hash: str):
    """
    Update user's password.
    """
    user.password_hash = new_password_hash

    db.commit()
    db.refresh(user)

    return user


def get_role_by_name(db: Session, role_name: str):
    """
    Fetch role by role name.
    """
    return (
        db.query(Role)
        .filter(Role.role_name == role_name)
        .first()
    )