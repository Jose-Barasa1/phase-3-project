from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

# Define the User model for registration and login
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    # Relationship to prescriptions
    prescriptions = relationship('Prescription', back_populates='user')

    def __repo__(self):
        return f"<User(id={self.id}, username={self.username})>"

# Define the Medicine model for storing medicine details
class Medicine(Base):
    __tablename__ = 'medicines'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    description = Column(String, nullable=True)
    category = Column(String, nullable=True)

    def __repr__(self):
        return f"<Medicine(name={self.name}, price={self.price}, category={self.category})>"

    @classmethod
    def create(cls, session, name, price, description, category):
        medicine = cls(name=name, price=price, description=description, category=category)
        session.add(medicine)
        session.commit()

    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()

    @classmethod
    def get_by_name(cls, session, name):
        return session.query(cls).filter(cls.name == name).first()

# Define the Prescription model to store user prescriptions
class Prescription(Base):
    __tablename__ = 'prescriptions'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    total_price = Column(Float, nullable=False)
    medicines = Column(String, nullable=False)  # Store medicine names as comma-separated string

    # Relationship to User model
    user = relationship('User', back_populates='prescriptions')

    def __init__(self, user_id, medicines, total_price):
        self.user_id = user_id
        self.medicines = ', '.join(medicines)  # Join list of medicines into a string
        self.total_price = total_price

    def __repo__(self):
        return f"<Prescription(id={self.id}, user_id={self.user_id}, total_price={self.total_price})>"
