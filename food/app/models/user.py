from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)

    role_id = Column(
        Integer,
        ForeignKey("roles.role_id"),
        nullable=False
    )

    first_name = Column(String(100), nullable=False)

    last_name = Column(String(100), nullable=False)

    email = Column(String(255), unique=True, nullable=False)

    password_hash = Column(String(255), nullable=False)

    phone = Column(String(15), unique=True, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    # Relationship with Role
    role = relationship("Role", back_populates="users")