from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.user import User
from app.repositories.user_repository import get_user_by_email, get_role_by_name
from app.auth.password import hash_password


def seed_super_admin():
    db: Session = SessionLocal()

    try:
        # Check if Super Admin already exists
        existing_user = get_user_by_email(
            db,
            "superadmin@gmail.com"
        )

        if existing_user:
            print("Super Admin already exists.")
            return

        # Get SUPER_ADMIN role
        role = get_role_by_name(
            db,
            "SUPER_ADMIN"
        )

        if role is None:
            print("SUPER_ADMIN role not found.")
            return

        # Create Super Admin
        super_admin = User(
            first_name="Super",
            last_name="Admin",
            email="superadmin@gmail.com",
            password_hash=hash_password("super@123"),
            phone="7904088015",
            role_id=role.role_id,
        )

        db.add(super_admin)
        db.commit()

        print("Super Admin created successfully.")

    finally:
        db.close()


if __name__ == "__main__":
    seed_super_admin()