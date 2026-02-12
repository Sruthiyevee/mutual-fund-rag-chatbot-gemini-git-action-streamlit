import sys
import os
import json
import numpy as np
from sentence_transformers import SentenceTransformer, util

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def debug():
    base_dir = "phase2_vector_db"
    vector_store_path = os.path.join(base_dir, "vector_store.json")
    embeddings_path = os.path.join(base_dir, "embeddings.npy")
    
    print(f"Loading vector store from {vector_store_path}")
    
    with open(vector_store_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    metadatas = data.get('metadatas', [])
    documents = data.get('documents', [])
    embeddings = np.load(embeddings_path)
    
    print(f"Loaded {len(metadatas)} chunks.")
    
    # Check for Service FAQs
    found_idx = -1
    target_text = "How can I download my Capital Gains Statement?"
    
    for i, doc in enumerate(documents):
        if target_text in doc:
            print(f"\nFOUND TARGET CHUNK at index {i}:")
            print(f"Metadata: {metadatas[i]}")
            print(f"Text: {doc[:200]}...")
            found_idx = i
            break
            
    if found_idx == -1:
        print(f"\nCRITICAL: Target text '{target_text}' NOT FOUND in vector store.")
        # Print first few docs to see what's in there
        print("First 3 docs:")
        for i in range(3):
            print(f"{i}: {documents[i][:100]}...")
        return

    # Check Similarity
    model = SentenceTransformer('all-MiniLM-L6-v2')
    query = "How can I download my capital gains statement?"
    query_embedding = model.encode(query, convert_to_tensor=True)
    
    chunk_embedding = embeddings[found_idx]
    # Ensure chunk_embedding is tensor or compatible
    score = util.cos_sim(query_embedding, chunk_embedding).item()
    
    print(f"\nSimilarity Score for query '{query}': {score:.4f}")
    print(f"Index of found chunk: {found_idx}")
    print(f"Chunk Text: {documents[found_idx][:100]}...")
    
    # Check Top K
    print("\nTop 5 Results for Query:")
    hits = util.semantic_search(query_embedding, embeddings, top_k=5)[0]
    for hit in hits:
        idx = hit['corpus_id']
        print(f"Index {idx}: Score {hit['score']:.4f}")
        print(f"Text: {documents[idx][:100]}...")
        if idx == found_idx:
            print("  -> THIS IS THE TARGET CHUNK!")

if __name__ == "__main__":
    debug()
