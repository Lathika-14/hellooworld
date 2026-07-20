from app.database import Base, engine

# Import models so SQLAlchemy knows about them
from app.models.role import Role
from app.models.user import User

Base.metadata.create_all(bind=engine)

print("✅ Tables created successfully!")