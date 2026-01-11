import os
import json
from typing import Dict, List
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv

load_dotenv()

# Initialize Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-pro",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.7,
    convert_system_message_to_human=True
)

# Quiz Generation Prompt Template
QUIZ_GENERATION_PROMPT = """You are an expert quiz creator. Based on the following Wikipedia article, create a comprehensive quiz.

Article Title: {title}

Article Content:
{content}

Article Sections: {sections}

Generate a JSON response with the following structure:
{{
    "summary": "A concise 2-3 sentence summary of the article",
    "key_entities": {{
        "people": ["list of important people mentioned"],
        "organizations": ["list of organizations mentioned"],
        "locations": ["list of locations mentioned"]
    }},
    "quiz": [
        {{
            "question": "Clear, specific question based on article content",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "answer": "The correct option text",
            "difficulty": "easy/medium/hard",
            "explanation": "Brief explanation referencing the article section or content"
        }}
    ],
    "related_topics": ["list of 5-7 related Wikipedia topics for further reading"]
}}

IMPORTANT REQUIREMENTS:
1. Generate exactly 8-10 quiz questions
2. Ensure questions have varying difficulty: 3-4 easy, 3-4 medium, 2-3 hard
3. All questions MUST be directly answerable from the article content - no hallucinations
4. Each explanation should reference specific sections or facts from the article
5. Options should be plausible but clearly distinguishable
6. Related topics should be actual Wikipedia topics related to the article
7. Key entities should be extracted from the actual article content
8. Return ONLY valid JSON, no additional text

Generate the quiz now:"""

# Entity Extraction Prompt (Fallback)
ENTITY_EXTRACTION_PROMPT = """Extract key entities from this Wikipedia article content.

Content: {content}

Return a JSON object with:
{{
    "people": ["list of people mentioned"],
    "organizations": ["list of organizations"],
    "locations": ["list of locations"]
}}

Return ONLY valid JSON:"""

# Related Topics Prompt (Fallback)
RELATED_TOPICS_PROMPT = """Based on this Wikipedia article about "{title}", suggest 5-7 related Wikipedia topics that would be interesting for further reading.

Article summary: {summary}

Return a JSON array of topic names:
["Topic 1", "Topic 2", "Topic 3", ...]

Return ONLY valid JSON array:"""

def extract_json_from_response(response_text: str) -> dict:
    """
    Extract JSON from LLM response, handling potential markdown formatting
    """
    try:
        # Try direct JSON parse
        return json.loads(response_text)
    except json.JSONDecodeError:
        # Try to extract JSON from markdown code blocks
        if "```json" in response_text:
            json_str = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            json_str = response_text.split("```")[1].split("```")[0].strip()
        else:
            json_str = response_text.strip()
        
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON: {e}")
            print(f"Response text: {response_text[:500]}")
            return None

def generate_quiz_from_content(title: str, content: str, sections: List[str]) -> Dict:
    """
    Generate quiz questions from Wikipedia article content using LLM
    
    Args:
        title: Article title
        content: Article content
        sections: List of section titles
        
    Returns:
        Dictionary containing quiz data
    """
    try:
        # Create prompt
        prompt = PromptTemplate(
            input_variables=["title", "content", "sections"],
            template=QUIZ_GENERATION_PROMPT
        )
        
        # Create chain
        chain = LLMChain(llm=llm, prompt=prompt)
        
        # Generate quiz
        sections_str = ", ".join(sections[:10])  # Limit sections in prompt
        response = chain.run(
            title=title,
            content=content[:10000],  # Limit content for token constraints
            sections=sections_str
        )
        
        # Parse response
        quiz_data = extract_json_from_response(response)
        
        if not quiz_data:
            # Fallback: Create basic quiz structure
            quiz_data = create_fallback_quiz(title, content, sections)
        
        # Validate and ensure required fields
        quiz_data.setdefault("summary", f"An article about {title}")
        quiz_data.setdefault("key_entities", {"people": [], "organizations": [], "locations": []})
        quiz_data.setdefault("quiz", [])
        quiz_data.setdefault("related_topics", [])
        
        # Validate quiz questions
        validated_quiz = []
        for q in quiz_data.get("quiz", []):
            if all(key in q for key in ["question", "options", "answer", "difficulty", "explanation"]):
                if len(q["options"]) == 4:
                    validated_quiz.append(q)
        
        quiz_data["quiz"] = validated_quiz[:10]  # Limit to 10 questions
        
        return quiz_data
        
    except Exception as e:
        print(f"Error generating quiz: {e}")
        # Return fallback quiz
        return create_fallback_quiz(title, content, sections)

def create_fallback_quiz(title: str, content: str, sections: List[str]) -> Dict:
    """
    Create a basic fallback quiz when LLM generation fails
    """
    return {
        "summary": f"This article discusses {title} and covers various aspects including {', '.join(sections[:3])}.",
        "key_entities": {
            "people": [],
            "organizations": [],
            "locations": []
        },
        "quiz": [
            {
                "question": f"What is the main topic of this article?",
                "options": [title, "Something else", "Unknown topic", "Not mentioned"],
                "answer": title,
                "difficulty": "easy",
                "explanation": "This is explicitly stated in the article title and introduction."
            }
        ],
        "related_topics": sections[:5] if sections else ["History", "Biography", "Science"]
    }

def validate_quiz_question(question: Dict) -> bool:
    """
    Validate a quiz question structure
    """
    required_keys = ["question", "options", "answer", "difficulty", "explanation"]
    
    if not all(key in question for key in required_keys):
        return False
    
    if len(question["options"]) != 4:
        return False
    
    if question["answer"] not in question["options"]:
        return False
    
    if question["difficulty"] not in ["easy", "medium", "hard"]:
        return False
    
    return True
