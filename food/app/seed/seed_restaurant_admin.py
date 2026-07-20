from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.user import User
from app.repositories.user_repository import (
    get_user_by_email,
    get_role_by_name,
)
from app.auth.password import hash_password


def seed_restaurant_admin():
    db: Session = SessionLocal()

    try:
        existing_user = get_user_by_email(
            db,
            "restaurant@gmail.com"
        )

        if existing_user:
            print("Restaurant Admin already exists.")
            return

        role = get_role_by_name(
            db,
            "RESTAURANT_ADMIN"
        )

        if role is None:
            print("RESTAURANT_ADMIN role not found.")
            return

        restaurant_admin = User(
            first_name="Restaurant",
            last_name="Admin",
            email="restaurant@gmail.com",
            password_hash=hash_password("restaurant@123"),
            phone="9524057555",
            role_id=role.role_id,
        )

        db.add(restaurant_admin)
        db.commit()

        print("Restaurant Admin created successfully.")

    finally:
        db.close()


if __name__ == "__main__":
    seed_restaurant_admin()