# init_db.py
from app.models import Base
from app.database import engine

if __name__ == "__main__":
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database initialized.")
