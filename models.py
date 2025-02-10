from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import os
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    password_hash = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    searches = relationship("RentSearch", back_populates="user")

class RentSearch(Base):
    __tablename__ = 'rent_searches'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    address = Column(String)
    zip_code = Column(String)
    current_rent = Column(Float)
    market_rate = Column(Float)
    rent_score = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="searches")

def init_db():
    """Initialize database and create all tables"""
    database_url = os.getenv('DATABASE_URL')
    if database_url:
        engine = create_engine(database_url)
        # Create all tables
        Base.metadata.create_all(engine)
        return engine
    else:
        raise ValueError("DATABASE_URL environment variable not set")

# Initialize database if this file is run directly
if __name__ == "__main__":
    init_db()