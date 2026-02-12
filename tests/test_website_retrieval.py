from phase3_retrieval.retrieval_pipeline import RetrievalSystem

# Test retrieval with website content
retriever = RetrievalSystem('phase2_vector_db')
results = retriever.retrieve('What is HDFC Midcap Fund?', k=5)

print('Query: What is HDFC Midcap Fund?\n')
print('Top 5 Results:\n')

for i, r in enumerate(results):
    print(f'{i+1}. Score: {r["score"]:.4f}')
    print(f'   Source: {r["metadata"].get("source_url", "N/A")}')
    print(f'   Source File: {r["metadata"].get("source_file", "N/A")}')
    print(f'   Text: {r["text"][:150]}...\n')
