import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from phase3_retrieval.retrieval_pipeline import RetrievalSystem

# Test retrieval for riskometer query
retriever = RetrievalSystem('phase2_vector_db')
results = retriever.retrieve('What is the riskometer rating of HDFC Large Cap Fund?', k=3)

print('Query: What is the riskometer rating of HDFC Large Cap Fund?')
print('\nTop 3 Retrieved Chunks:')
print('=' * 80)

for i, result in enumerate(results, 1):
    print(f'\n{i}. Score: {result["score"]:.4f}')
    print(f'   Source: {result["metadata"].get("source_url", "Unknown")}')
    print(f'   Text Preview: {result["text"][:200]}...')
    print('-' * 80)
