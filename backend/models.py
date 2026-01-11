from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# Database configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/wiki_quiz_db"
)

# Handle Vercel PostgreSQL URL format (postgres:// -> postgresql://)
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class QuizRecord(Base):
    """
    Database model for storing quiz records
    """
    __tablename__ = "quiz_records"
    
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    summary = Column(Text)
    key_entities = Column(JSON)  # Stores {"people": [], "organizations": [], "locations": []}
    sections = Column(JSON)  # List of section titles
    quiz = Column(JSON, nullable=False)  # List of quiz questions
    related_topics = Column(JSON)  # List of related Wikipedia topics
    raw_html = Column(Text, nullable=True)  # Optional: store raw HTML
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<QuizRecord(id={self.id}, title='{self.title}', url='{self.url}')>"
