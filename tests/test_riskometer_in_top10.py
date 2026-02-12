import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from phase3_retrieval.retrieval_pipeline import RetrievalSystem
from dotenv import load_dotenv

load_dotenv()

# Initialize retriever
retriever = RetrievalSystem('phase2_vector_db')

# Test riskometer query with more results
query = "What is the riskometer rating of HDFC Small Cap Fund?"
results = retriever.retrieve(query, k=10)

output_lines = []
output_lines.append(f"QUERY: {query}")
output_lines.append("="*80)

for i, result in enumerate(results, 1):
    output_lines.append(f"\n{i}. Score: {result['score']:.4f} | Scheme: {result['metadata'].get('scheme', 'Unknown')}")
    if "riskometer" in result['text'].lower() or "very high" in result['text'].lower():
        output_lines.append(f"   ✓ Contains riskometer/rating info")
        output_lines.append(f"   Text preview: {result['text'][:200]}...")

# Write to file
with open('test_riskometer_retrieval.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output_lines))

print("Output written to test_riskometer_retrieval.txt")
