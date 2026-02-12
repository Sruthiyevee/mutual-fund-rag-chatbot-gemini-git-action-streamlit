import os
import sys
import logging
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import random

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from phase3_retrieval.retrieval_pipeline import RetrievalSystem
from phase4_generation.generation_pipeline import AnswerGenerator

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()

app = FastAPI(title="MF Facts API", description="Facts-only Mutual Fund Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG Components
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
EMBEDDINGS_DIR = os.path.join(BASE_DIR, "phase2_vector_db")

if not os.path.exists(EMBEDDINGS_DIR):
    logging.error(f"Embeddings directory not found at {EMBEDDINGS_DIR}")
    raise RuntimeError("Embeddings directory not found. Please run Phase 2 first.")

logging.info("Initializing Retrieval System...")
retriever = RetrievalSystem(EMBEDDINGS_DIR)

logging.info("Initializing Generator...")
generator = AnswerGenerator()

# Data Models
class ChatRequest(BaseModel):
    message: str
    session_id: str

class ChatResponse(BaseModel):
    answer: str
    sources: List[str]
    suggestions: List[str]

# Fallback Suggestions
FALLBACK_QUESTIONS = [
    "What is the investment objective of HDFC Large Cap Fund?",
    "What are the risks associated with mutual funds?",
    "Who is eligible to invest in HDFC Mutual Fund?",
    "How is NAV calculated?",
    "What is a Systematic Investment Plan (SIP)?"
]

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        query = request.message.strip()
        if not query:
            raise HTTPException(status_code=400, detail="Message cannot be empty")

        # Conversational / Acknowledgement Handling
        conversational_triggers = {"ok", "okay", "thanks", "thank you", "got it", "thx", "cheers", "cool", "👍", "yes"}
        cleaned_query = "".join(char for char in query.lower() if char.isalnum() or char.isspace()).strip()
        
        if cleaned_query in conversational_triggers:
            return ChatResponse(
                answer="You’re welcome! 🙂 What else would you like to know about mutual funds?",
                sources=[],
                suggestions=[]
            )

        # Phase 3: Retrieve
        logging.info(f"Retrieving for: {query}")
        chunks = retriever.retrieve(query, k=5)
        
        # Phase 4: Generate
        logging.info("Generating answer...")
        answer = generator.generate_answer(query, chunks)
        
        # Extract sources (prioritize URL, then filename)
        sources = list(set([
            chunk.get('metadata', {}).get('source_url') or 
            chunk.get('metadata', {}).get('source_file') or 
            'Unknown Source'
            for chunk in chunks
        ]))
        
        # Filter out empty strings if any
        sources = [s for s in sources if s]
        
        # Check for fallback response
        suggestions = []
        if "I don't know based on the provided sources" in answer:
            suggestions = random.sample(FALLBACK_QUESTIONS, 3)
            
        return ChatResponse(
            answer=answer,
            sources=sources,
            suggestions=suggestions
        )

    except Exception as e:
        logging.error(f"Error processing chat request: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
