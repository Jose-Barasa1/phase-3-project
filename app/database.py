from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database URI 
DATABASE_URI = 'sqlite:///medhub.db'

# Create the engine to connect to the database
engine = create_engine(DATABASE_URI, echo=True)

# Create a base class for our models
Base = declarative_base()

# Session for querying the database
Session = sessionmaker(bind=engine)

def init_db():
    """Create all tables in the database."""
    Base.metadata.create_all(engine)


