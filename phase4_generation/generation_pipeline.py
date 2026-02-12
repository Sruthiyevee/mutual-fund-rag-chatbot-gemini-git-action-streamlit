import os
import logging
from typing import List, Dict, Any
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AnswerGenerator:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            logging.warning("GEMINI_API_KEY not found. Helper will fail if actual generation is attempted.")
            self.model = None
        else:
            try:
                genai.configure(api_key=self.api_key)
                # Using Gemini 2.0 Flash for speed and efficiency, or fall back to Pro if needed.
                self.model = genai.GenerativeModel('gemini-2.0-flash')
            except Exception as e:
                logging.error(f"Failed to initialize Gemini client: {e}")
                self.model = None
        
        self.system_prompt = """You are a helpful and friendly Mutual Fund FAQ assistant.

CORE RULES:
- Answer using ONLY the provided context.
- Be warm and human-like. Use 1–2 simple emojis (e.g., 🙂, 📘) to be friendly.
- Provide NO investment advice or opinions.
- Keep responses concise (≤ 3 sentences).
- Do NOT include citations or "Source:" inside your text response. The system handles citations separately.

EXTRACTING SPECIFIC FACTS:
When asked about specific facts (expense ratios, riskometer ratings, exit loads, minimum SIP amounts, etc.):
1. Carefully scan the context for the EXACT information requested
2. Look for numerical values, percentages, ratings, or specific terms
3. If found, state it directly and clearly (e.g., "The expense ratio is 1.61% p.a." or "The riskometer rating is Very High (Level 6 out of 6)")
4. Only say "I don't know" if the specific fact is truly absent from the context

FORBIDDEN ACTIONS:
- Never recommend or compare mutual funds
- Never predict or calculate returns
- Never use persuasive or advisory language
- Never use external or prior knowledge

If information is missing or irrelevant, strictly state: "I don't know based on the provided sources 🙂"
"""

    def generate_answer(self, query: str, retrieved_chunks: List[Dict[str, Any]]) -> str:
        """
        Generate an answer using Gemini based on the query and retrieved chunks.
        """
        if not self.model:
            return "Reference Code: MISSING_API_KEY. Please set GEMINI_API_KEY to generate real answers."

        if not retrieved_chunks:
            return "I don't know based on the provided sources. Please ask an alternative question to search."

        # Step 1: Context Assembly
        context_str = self._build_context_str(retrieved_chunks)
        
        # Step 2: Prompt Construction
        # Gemini favors a single prompt string or chat history. For strict RAG, we'll combine system + context + query.
        full_prompt = f"{self.system_prompt}\n\nCONTEXT:\n{context_str}\n\nUSER QUESTION: {query}"
        
        # Step 3: LLM Invocation
        try:
            response = self.model.generate_content(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.0, # Deterministic
                    max_output_tokens=300
                )
            )
            return response.text
            
        except Exception as e:
            error_details = f"Error generating answer: {type(e).__name__}: {str(e)}"
            logging.error(error_details)
            # Return detailed error for debugging
            return f"Sorry, I encountered an error while generating the response. Details: {str(e)}"

    def _build_context_str(self, chunks: List[Dict[str, Any]]) -> str:
        """Helper to format context with sources."""
        context_parts = []
        for chunk in chunks:
            source = chunk.get('metadata', {}).get('source_file', 'Unknown Source')
            text = chunk.get('text', '')
            context_parts.append(f"Source: {source}\nContent: {text}")
        return "\n\n".join(context_parts)
