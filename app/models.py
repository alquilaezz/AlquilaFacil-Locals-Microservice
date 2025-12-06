from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    Text,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from .database import Base

class LocalCategory(Base):
    __tablename__ = "local_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)
    photo_url = Column(Text, nullable=True)

    locals = relationship("Local", back_populates="category")

class Local(Base):
    __tablename__ = "locals"

    id = Column(Integer, primary_key=True, index=True)
    local_name = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    country = Column(Text, nullable=False)
    city = Column(Text, nullable=False)
    district = Column(Text, nullable=False)
    street = Column(Text, nullable=False)
    price_per_hour = Column(Text, nullable=False)
    capacity = Column(Text, nullable=False)
    features = Column(Text, nullable=True)  # puedes guardar JSON o texto plano
    local_category_id = Column(Integer, ForeignKey("local_categories.id"), nullable=False)
    user_id = Column(Integer, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    category = relationship("LocalCategory", back_populates="locals")
    photos = relationship("LocalPhoto", back_populates="local", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="local", cascade="all, delete-orphan")

class LocalPhoto(Base):
    __tablename__ = "local_photos"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(Text, nullable=False)
    local_id = Column(Integer, ForeignKey("locals.id"), nullable=False)

    local = relationship("Local", back_populates="photos")

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    local_id = Column(Integer, ForeignKey("locals.id"), nullable=False, index=True)
    text = Column(Text, nullable=False)
    rating = Column(Integer, nullable=False)

    local = relationship("Local", back_populates="comments")
