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

output_lines = []

for query in test_queries:
    output_lines.append(f"\n{'='*80}")
    output_lines.append(f"QUERY: {query}")
    output_lines.append('='*80)
    
    # Retrieve
    results = retriever.retrieve(query, k=3)
    
    output_lines.append(f"\nRetrieved {len(results)} chunks with scores: {[f'{r['score']:.4f}' for r in results]}")
    
    # Generate answer
    output_lines.append("\nGENERATED ANSWER:")
    output_lines.append("-"*80)
    answer = generator.generate_answer(query, results)
    output_lines.append(answer)
    output_lines.append("-"*80)

# Write to file
with open('test_answer_output.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output_lines))

print("Output written to test_answer_output.txt")
