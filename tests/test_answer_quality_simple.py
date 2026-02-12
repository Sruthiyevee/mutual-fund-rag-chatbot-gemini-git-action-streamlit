import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from phase3_retrieval.retrieval_pipeline import RetrievalSystem
from phase4_generation.generation_pipeline import AnswerGenerator
from dotenv import load_dotenv

load_dotenv()

# Initialize systems
retriever = RetrievalSystem('phase2_vector_db')
generator = AnswerGenerator()

# Test queries
test_queries = [
    "What is the expense ratio of HDFC Midcap Fund?",
    "What is the riskometer rating of HDFC Small Cap Fund?"
]

for query in test_queries:
    print(f"\n{'='*80}")
    print(f"QUERY: {query}")
    print('='*80)
    
    # Retrieve
    results = retriever.retrieve(query, k=3)
    
    print(f"\nRetrieved {len(results)} chunks with scores: {[f'{r['score']:.4f}' for r in results]}")
    
    # Generate answer
    print("\nGENERATED ANSWER:")
    print("-"*80)
    answer = generator.generate_answer(query, results)
    print(answer)
    print("-"*80)
