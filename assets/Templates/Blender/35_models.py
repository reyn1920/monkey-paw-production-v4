"""
Domain models for VidScript Pro application.
"""
from datetime import datetime
from enum import Enum
from typing import Optional, List
from uuid import UUID, uuid4

from sqlalchemy import Column, String, DateTime, Boolean, Integer, Text, ForeignKey, Float
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()


class UserRole(str, Enum):
    """User role enumeration."""
    ADMIN = "admin"
    USER = "user"
    PREMIUM = "premium"


class ProjectStatus(str, Enum):
    """Project status enumeration."""
    DRAFT = "draft"
    RESEARCH = "research"
    SCRIPTING = "scripting"
    PRODUCTION = "production"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class User(Base):
    """User model."""
    __tablename__ = "users"
    
    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    role = Column(String(20), default=UserRole.USER, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    projects = relationship("Project", back_populates="owner", cascade="all, delete-orphan")
    channels = relationship("Channel", back_populates="owner", cascade="all, delete-orphan")


class Channel(Base):
    """YouTube channel model."""
    __tablename__ = "channels"
    
    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(255), nullable=False)
    youtube_channel_id = Column(String(100), unique=True, nullable=True)
    description = Column(Text, nullable=True)
    subscriber_count = Column(Integer, default=0, nullable=False)
    video_count = Column(Integer, default=0, nullable=False)
    view_count = Column(Integer, default=0, nullable=False)
    owner_id = Column(PostgresUUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    owner = relationship("User", back_populates="channels")
    projects = relationship("Project", back_populates="channel")


class Project(Base):
    """Video project model."""
    __tablename__ = "projects"
    
    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(20), default=ProjectStatus.DRAFT, nullable=False)
    target_keywords = Column(Text, nullable=True)  # JSON string of keywords
    target_audience = Column(String(255), nullable=True)
    estimated_views = Column(Integer, default=0, nullable=False)
    estimated_revenue = Column(Float, default=0.0, nullable=False)
    owner_id = Column(PostgresUUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    channel_id = Column(PostgresUUID(as_uuid=True), ForeignKey("channels.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    owner = relationship("User", back_populates="projects")
    channel = relationship("Channel", back_populates="projects")
    research_data = relationship("ResearchData", back_populates="project", cascade="all, delete-orphan")


class ResearchData(Base):
    """Research data for projects."""
    __tablename__ = "research_data"
    
    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    keyword = Column(String(255), nullable=False)
    search_volume = Column(Integer, default=0, nullable=False)
    competition_score = Column(Float, default=0.0, nullable=False)
    trend_data = Column(Text, nullable=True)  # JSON string of trend data
    project_id = Column(PostgresUUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    project = relationship("Project", back_populates="research_data")