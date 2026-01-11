from pydantic import BaseModel, HttpUrl, Field
from typing import List, Dict, Optional, Any
from datetime import datetime

class QuizRequest(BaseModel):
    """Request model for quiz generation"""
    url: str = Field(..., description="Wikipedia article URL")
    force_regenerate: bool = Field(False, description="Force regenerate even if cached")
    store_raw_html: bool = Field(False, description="Store raw HTML in database")

class QuizQuestion(BaseModel):
    """Model for a single quiz question"""
    question: str
    options: List[str]
    answer: str
    difficulty: str
    explanation: str

class KeyEntities(BaseModel):
    """Model for extracted key entities"""
    people: List[str] = []
    organizations: List[str] = []
    locations: List[str] = []

class QuizResponse(BaseModel):
    """Response model for quiz data"""
    id: int
    url: str
    title: str
    summary: str
    key_entities: Dict[str, List[str]]
    sections: List[str]
    quiz: List[Dict[str, Any]]
    related_topics: List[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

class QuizHistoryResponse(BaseModel):
    """Response model for quiz history listing"""
    id: int
    url: str
    title: str
    created_at: datetime
    quiz_count: int
    
    class Config:
        from_attributes = True
