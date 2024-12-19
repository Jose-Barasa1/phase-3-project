from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Model: User
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username})>"

    @classmethod
    def create(cls, session, username, password):
        user = cls(username=username, password=password)
        session.add(user)
        session.commit()
        return user

    @classmethod
    def find_by_username(cls, session, username):
        return session.query(cls).filter_by(username=username).first()

# Model: Medicine
class Medicine(Base):
    __tablename__ = 'medicines'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=False)

    def __repr__(self):
        return f"<Medicine(id={self.id}, name={self.name}, description={self.description})>"

    @classmethod
    def create(cls, session, name, description):
        medicine = cls(name=name, description=description)
        session.add(medicine)
        session.commit()

    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()

    @classmethod
    def search_by_name(cls, session, name):
        return session.query(cls).filter(Medicine.name.like(f'%{name}%')).all()

# Model: Prescription
class Prescription(Base):
    __tablename__ = 'prescriptions'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    diagnosis = Column(String, nullable=False)
    prescribed_medicines = Column(String, nullable=False)

    user = relationship("User", back_populates="prescriptions")

    def __repr__(self):
        return f"<Prescription(id={self.id}, user_id={self.user_id}, diagnosis={self.diagnosis})>"

    @classmethod
    def create(cls, session, user_id, diagnosis, prescribed_medicines):
        prescription = cls(user_id=user_id, diagnosis=diagnosis, prescribed_medicines=prescribed_medicines)
        session.add(prescription)
        session.commit()

# Create relationship back reference in User
User.prescriptions = relationship("Prescription", back_populates="user")
