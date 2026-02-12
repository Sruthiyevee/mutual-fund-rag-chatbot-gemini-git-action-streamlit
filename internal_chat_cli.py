import os
import sys
from dotenv import load_dotenv

# Ensure parent directory is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from phase3_retrieval.retrieval_pipeline import RetrievalSystem
from phase4_generation.generation_pipeline import AnswerGenerator

def main():
    load_dotenv()
    
    # Initialize components
    base_dir = os.path.dirname(os.path.abspath(__file__))
    embeddings_dir = os.path.join(base_dir, "phase2_vector_db")
    
    # Check if retrieval system exists (Phase 3)
    if not os.path.exists(embeddings_dir):
        print(f"Error: Embeddings directory not found at {embeddings_dir}")
        return

    print("Initializing Retrieval System...")
    retriever = RetrievalSystem(embeddings_dir)
    
    print("Initializing Generator...")
    # Will warn if API key is missing, handled gracefully
    generator = AnswerGenerator() 
    
    # User Interface Elements
    print("\n" + "="*60)
    print("Welcome to the Mutual Fund FAQ Assistant!")
    print("I can answer factual questions based on HDFC and AMFI documents.")
    print("Disclaimer: Facts-only. No investment advice.")
    print("-" * 60)
    print("Example Questions:")
    print("1. What is the investment objective of HDFC Top 100 Fund?")
    print("2. What are the risks associated with mutual funds?")
    print("3. How are equity funds categorized?")
    print("="*60 + "\n")
    
    while True:
        try:
            query = input("\nYour Question (or 'quit'): ").strip()
            if query.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            
            if not query:
                continue
            
            # Phase 3: Retrieve
            print("Searching... ", end="", flush=True)
            chunks = retriever.retrieve(query, k=5)
            print(f"Found {len(chunks)} relevant contexts.")
            
            # Phase 4: Generate
            print("Thinking... ", end="", flush=True)
            answer = generator.generate_answer(query, chunks)
            
            # Output
            print("\n" + "-"*40)
            print(answer)
            print("-" * 40)
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}")

if __name__ == "__main__":
    main()
