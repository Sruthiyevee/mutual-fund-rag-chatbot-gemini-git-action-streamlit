import sys
import os
import json

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from phase3_retrieval.retrieval_pipeline import RetrievalSystem

def test_retrieval():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    embeddings_dir = os.path.join(base_dir, "phase2_vector_db")
    
    if not os.path.exists(embeddings_dir):
        print(f"Error: Embeddings directory not found at {embeddings_dir}")
        return

    print("Initializing Retrieval System...")
    retriever = RetrievalSystem(embeddings_dir)
    
    query = "What is the investment objective of HDFC Large Cap Fund?"
    print(f"\nRetrieving for: '{query}'")
    chunks = retriever.retrieve(query, k=3)
    
    print(f"\nRetrieved {len(chunks)} chunks:")
    for i, chunk in enumerate(chunks):
        print(f"\nChunk {i+1}:")
        print(f"Text Snippet: {chunk.get('text', '')[:100]}...")
        print(f"Metadata: {json.dumps(chunk.get('metadata', {}), indent=2)}")
        print(f"Source File: '{chunk.get('metadata', {}).get('source', 'KEY_NOT_FOUND')}'")
        print(f"Source File (alt): '{chunk.get('metadata', {}).get('source_file', 'KEY_NOT_FOUND')}'")

if __name__ == "__main__":
    test_retrieval()
