from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import sys

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from dotenv import load_dotenv
load_dotenv()

app = FastAPI(
    title="Wikipedia Quiz Generator API",
    description="Generate quizzes from Wikipedia articles using AI",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api")
async def root():
    return {
        "message": "Wikipedia Quiz Generator API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/api/health")
async def health():
    return {"status": "healthy"}

# Import routes from backend
try:
    from scraper import scrape_wikipedia
    from quiz_generator import generate_quiz_from_content
    from pydantic import BaseModel
    from typing import List, Optional, Dict, Any
    
    class QuizRequest(BaseModel):
        url: str
    
    class QuizResponse(BaseModel):
        id: Optional[int] = None
        title: str
        url: str
        summary: str
        key_entities: Dict[str, Any]
        quiz: List[Dict[str, Any]]
        related_topics: List[str]
        created_at: Optional[str] = None
    
    @app.post("/api/generate-quiz", response_model=QuizResponse)
    async def generate_quiz(request: QuizRequest):
        """Generate a quiz from a Wikipedia URL"""
        try:
            # Validate URL
            if not request.url.startswith("https://en.wikipedia.org/wiki/"):
                raise HTTPException(
                    status_code=400,
                    detail="Invalid URL. Please provide a valid English Wikipedia article URL."
                )
            
            # Scrape Wikipedia article
            article_data = scrape_wikipedia(request.url)
            
            if not article_data:
                raise HTTPException(
                    status_code=404,
                    detail="Could not scrape the Wikipedia article. Please check the URL."
                )
            
            # Generate quiz using LLM
            quiz_data = generate_quiz_from_content(
                title=article_data["title"],
                content=article_data["content"],
                sections=article_data["sections"]
            )
            
            response = QuizResponse(
                title=article_data["title"],
                url=request.url,
                summary=quiz_data.get("summary", ""),
                key_entities=quiz_data.get("key_entities", {}),
                quiz=quiz_data.get("quiz", []),
                related_topics=quiz_data.get("related_topics", [])
            )
            
            return response
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error generating quiz: {str(e)}")
    
    @app.get("/api/history")
    async def get_history():
        """Get quiz history - returns empty for serverless"""
        return []
    
    @app.get("/api/quiz/{quiz_id}")
    async def get_quiz(quiz_id: int):
        """Get a specific quiz by ID - not available in serverless mode"""
        raise HTTPException(status_code=404, detail="Quiz history not available in serverless mode")

except ImportError as e:
    print(f"Warning: Could not import backend modules: {e}")
    
    @app.post("/api/generate-quiz")
    async def generate_quiz_fallback():
        raise HTTPException(status_code=503, detail="Backend modules not available")
