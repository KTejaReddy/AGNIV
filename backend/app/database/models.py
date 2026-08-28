from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.sql import func
from .session import Base

class Setting(Base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, index=True, nullable=False)
    value = Column(Text, nullable=True) # JSON encoded string for flexibility

class Permission(Base):
    __tablename__ = "permissions"
    
    id = Column(Integer, primary_key=True, index=True)
    capability_name = Column(String, unique=True, index=True, nullable=False)
    rule = Column(String, nullable=False) # ALWAYS_ALLOW, ASK, NEVER_ALLOW, SESSION_ONLY

class Session(Base):
    __tablename__ = "sessions"
    
    id = Column(String, primary_key=True, index=True) # UUID string
    created_at = Column(DateTime, server_default=func.now())
    active = Column(Boolean, default=True)
    workspace_data = Column(Text, nullable=True) # JSON payload of context

