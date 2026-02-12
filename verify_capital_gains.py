import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from phase3_retrieval.retrieval_pipeline import RetrievalSystem

def verify():
    print("Initializing Retrieval System...")
    embeddings_dir = "phase2_vector_db"
    retriever = RetrievalSystem(embeddings_dir)
    
    query = "How can I download my capital gains statement?"
    print(f"\nQuerying: {query}")
    
    results = retriever.retrieve(query, k=3)
    
    found = False
    for res in results:
        print(f"\n[Score: {res['score']:.4f}]")
        print(f"Source: {res['metadata']['source_url']}")
        print(f"Text Preview: {res['text'][:100]}...")
        
        if "capital gains" in res['text'].lower() and "download" in res['text'].lower():
            found = True
            
    if found:
        print("\nSUCCESS: Found relevant information about capital gains statement.")
    else:
        print("\nFAILURE: Did not find relevant information.")
        print("Debugging: List of files in vector store:")
        # In a real scenario we'd check self.documents or metadata
        
if __name__ == "__main__":
    verify()
