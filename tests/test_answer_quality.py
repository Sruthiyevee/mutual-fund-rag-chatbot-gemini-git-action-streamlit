import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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
    
    print("\nTop 3 Retrieved Chunks:")
    for i, result in enumerate(results, 1):
        print(f"\n{i}. Score: {result['score']:.4f}")
        print(f"   Source: {result['metadata'].get('category', 'Unknown')}")
        print(f"   Text: {result['text'][:300]}...")
    
    # Generate answer
    print("\n" + "-"*80)
    print("GENERATED ANSWER:")
    print("-"*80)
    answer = generator.generate_answer(query, results)
    print(answer['answer'])
    print(f"\nSources: {answer.get('sources', [])}")
