import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from phase3_retrieval.retrieval_pipeline import RetrievalSystem
from dotenv import load_dotenv

load_dotenv()

# Initialize retriever
retriever = RetrievalSystem('phase2_vector_db')

# Test queries
test_queries = [
    "What is the expense ratio of HDFC Midcap Fund?",
    "What is the riskometer rating of HDFC Small Cap Fund?"
]

output_lines = []

for query in test_queries:
    output_lines.append(f"\n{'='*80}")
    output_lines.append(f"QUERY: {query}")
    output_lines.append('='*80)
    
    # Retrieve
    results = retriever.retrieve(query, k=3)
    
    for i, result in enumerate(results, 1):
        output_lines.append(f"\n{i}. Score: {result['score']:.4f}")
        output_lines.append(f"   Category: {result['metadata'].get('category', 'Unknown')}")
        output_lines.append(f"   Scheme: {result['metadata'].get('scheme', 'Unknown')}")
        output_lines.append(f"\n   FULL TEXT:")
        output_lines.append(f"   {result['text']}")
        output_lines.append("-" * 80)

# Write to file
with open('test_retrieved_chunks.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output_lines))

print("Chunks written to test_retrieved_chunks.txt")
