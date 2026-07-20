from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.user import User
from app.repositories.user_repository import (
    get_user_by_email,
    get_role_by_name,
)
from app.auth.password import hash_password


def seed_delivery_agent():
    db: Session = SessionLocal()

    try:
        existing_user = get_user_by_email(
            db,
            "delivery@gmail.com"
        )

        if existing_user:
            print("Delivery Agent already exists.")
            return

        role = get_role_by_name(
            db,
            "DELIVERY_AGENT"
        )

        if role is None:
            print("DELIVERY_AGENT role not found.")
            return

        delivery_agent = User(
            first_name="Delivery",
            last_name="Agent",
            email="delivery@gmail.com",
            password_hash=hash_password("delivery@123"),
            phone="9236789762",
            role_id=role.role_id,
        )

        db.add(delivery_agent)
        db.commit()

        print("Delivery Agent created successfully.")

    finally:
        db.close()


if __name__ == "__main__":
    seed_delivery_agent()