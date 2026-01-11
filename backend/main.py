from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import os
from dotenv import load_dotenv

from models import QuizRecord, SessionLocal, engine, Base
from scraper import scrape_wikipedia
from quiz_generator import generate_quiz_from_content
from schemas import QuizRequest, QuizResponse, QuizHistoryResponse

# Load environment variables
load_dotenv()

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Wikipedia Quiz Generator API",
    description="Generate quizzes from Wikipedia articles using AI",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {
        "message": "Wikipedia Quiz Generator API",
        "version": "1.0.0",
        "endpoints": {
            "generate_quiz": "/api/generate-quiz",
            "get_history": "/api/history",
            "get_quiz_by_id": "/api/quiz/{id}"
        }
    }

@app.post("/api/generate-quiz", response_model=QuizResponse)
async def generate_quiz(request: QuizRequest, db: Session = Depends(get_db)):
    """
    Generate a quiz from a Wikipedia article URL
    """
    try:
        # Check if URL already exists in database (caching)
        existing_quiz = db.query(QuizRecord).filter(
            QuizRecord.url == request.url
        ).first()
        
        if existing_quiz and not request.force_regenerate:
            # Return cached quiz
            return QuizResponse(
                id=existing_quiz.id,
                url=existing_quiz.url,
                title=existing_quiz.title,
                summary=existing_quiz.summary,
                key_entities=existing_quiz.key_entities,
                sections=existing_quiz.sections,
                quiz=existing_quiz.quiz,
                related_topics=existing_quiz.related_topics,
                created_at=existing_quiz.created_at
            )
        
        # Scrape Wikipedia article
        scraped_data = scrape_wikipedia(request.url)
        
        if not scraped_data:
            raise HTTPException(
                status_code=400,
                detail="Failed to scrape Wikipedia article. Please check the URL."
            )
        
        # Generate quiz using LLM
        quiz_data = generate_quiz_from_content(
            title=scraped_data["title"],
            content=scraped_data["content"],
            sections=scraped_data["sections"]
        )
        
        # Prepare data for storage
        quiz_record_data = {
            "url": request.url,
            "title": scraped_data["title"],
            "summary": quiz_data.get("summary", scraped_data.get("summary", "")),
            "key_entities": quiz_data.get("key_entities", {}),
            "sections": scraped_data["sections"],
            "quiz": quiz_data["quiz"],
            "related_topics": quiz_data.get("related_topics", []),
            "raw_html": scraped_data.get("raw_html", "") if request.store_raw_html else None
        }
        
        # Save to database
        if existing_quiz:
            # Update existing record
            for key, value in quiz_record_data.items():
                setattr(existing_quiz, key, value)
            db.commit()
            db.refresh(existing_quiz)
            quiz_record = existing_quiz
        else:
            # Create new record
            quiz_record = QuizRecord(**quiz_record_data)
            db.add(quiz_record)
            db.commit()
            db.refresh(quiz_record)
        
        return QuizResponse(
            id=quiz_record.id,
            url=quiz_record.url,
            title=quiz_record.title,
            summary=quiz_record.summary,
            key_entities=quiz_record.key_entities,
            sections=quiz_record.sections,
            quiz=quiz_record.quiz,
            related_topics=quiz_record.related_topics,
            created_at=quiz_record.created_at
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating quiz: {str(e)}"
        )

@app.get("/api/history", response_model=List[QuizHistoryResponse])
async def get_history(db: Session = Depends(get_db)):
    """
    Get all quiz history
    """
    try:
        quizzes = db.query(QuizRecord).order_by(QuizRecord.created_at.desc()).all()
        return [
            QuizHistoryResponse(
                id=quiz.id,
                url=quiz.url,
                title=quiz.title,
                created_at=quiz.created_at,
                quiz_count=len(quiz.quiz) if quiz.quiz else 0
            )
            for quiz in quizzes
        ]
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching history: {str(e)}"
        )

@app.get("/api/quiz/{quiz_id}", response_model=QuizResponse)
async def get_quiz_by_id(quiz_id: int, db: Session = Depends(get_db)):
    """
    Get a specific quiz by ID
    """
    try:
        quiz = db.query(QuizRecord).filter(QuizRecord.id == quiz_id).first()
        
        if not quiz:
            raise HTTPException(
                status_code=404,
                detail="Quiz not found"
            )
        
        return QuizResponse(
            id=quiz.id,
            url=quiz.url,
            title=quiz.title,
            summary=quiz.summary,
            key_entities=quiz.key_entities,
            sections=quiz.sections,
            quiz=quiz.quiz,
            related_topics=quiz.related_topics,
            created_at=quiz.created_at
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching quiz: {str(e)}"
        )

@app.delete("/api/quiz/{quiz_id}")
async def delete_quiz(quiz_id: int, db: Session = Depends(get_db)):
    """
    Delete a quiz by ID
    """
    try:
        quiz = db.query(QuizRecord).filter(QuizRecord.id == quiz_id).first()
        
        if not quiz:
            raise HTTPException(
                status_code=404,
                detail="Quiz not found"
            )
        
        db.delete(quiz)
        db.commit()
        
        return {"message": "Quiz deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error deleting quiz: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
