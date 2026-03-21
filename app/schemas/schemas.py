from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Auth Schemas
class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role_id: int

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# Task Schemas
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    assigned_to: int

class TaskUpdate(BaseModel):
    status: str

class TaskOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: str
    assigned_to: int
    created_at: datetime

    class Config:
        from_attributes = True

# Document Schemas
class DocumentOut(BaseModel):
    id: int
    filename: str
    uploaded_at: datetime

    class Config:
        from_attributes = True

# Search Schema
class SearchQuery(BaseModel):
    query: str

# Analytics Schema
class AnalyticsOut(BaseModel):
    total_tasks: int
    completed_tasks: int
    pending_tasks: int
    total_searches: int
    total_documents: int