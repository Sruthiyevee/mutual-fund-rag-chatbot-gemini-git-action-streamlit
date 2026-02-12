import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from phase3_retrieval.retrieval_pipeline import RetrievalSystem

# Test retrieval for riskometer query
retriever = RetrievalSystem('phase2_vector_db')
results = retriever.retrieve('What is the riskometer rating of HDFC Large Cap Fund?', k=5)

print('Query: What is the riskometer rating of HDFC Large Cap Fund?')
print('\nTop 5 Retrieved Chunks:')
print('=' * 80)

for i, result in enumerate(results, 1):
    print(f'\n{i}. Score: {result["score"]:.4f}')
    print(f'   Source: {result["metadata"].get("source_file", "Unknown")}')
    print(f'   Text: {result["text"][:300]}...')
    print('-' * 80)
