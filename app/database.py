from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

DATABASE_URL = "sqlite:///medicine_cli.db"  # SQLite database

# Setup the database connection
engine = create_engine(DATABASE_URL, echo=True)

# Create a sessionmaker instance
Session = sessionmaker(bind=engine)

def init_db():
    """Create all tables"""
    Base.metadata.create_all(engine)
