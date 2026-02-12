import os
import json
import numpy as np
import logging
from typing import List, Dict, Any, Tuple
from sentence_transformers import SentenceTransformer, util

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class RetrievalSystem:
    def __init__(self, embeddings_dir: str):
        self.embeddings_dir = embeddings_dir
        self.vector_store_path = os.path.join(embeddings_dir, "vector_store.json")
        self.embeddings_path = os.path.join(embeddings_dir, "embeddings.npy")
        
        self.documents = []
        self.metadatas = []
        self.embeddings = None
        self.ids = []
        
        self._load_artifacts()
        
        # Initialize Embedding Model (same as Phase 2)
        # We use CPU by default for stability, can be configured for cuda if needed
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def _load_artifacts(self):
        """Load the persisted vector store and embeddings."""
        try:
            # Load structured data
            if not os.path.exists(self.vector_store_path):
                raise FileNotFoundError(f"Vector store not found at {self.vector_store_path}")
            
            with open(self.vector_store_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.documents = data.get('documents', [])
                self.metadatas = data.get('metadatas', [])
                self.ids = data.get('ids', [])
            
            # Load embeddings
            if not os.path.exists(self.embeddings_path):
                raise FileNotFoundError(f"Embeddings not found at {self.embeddings_path}")
            
            self.embeddings = np.load(self.embeddings_path)
            
            logging.info(f"Loaded {len(self.ids)} chunks from {self.embeddings_dir}")
            
        except Exception as e:
            logging.error(f"Error loading artifacts: {e}")
            raise

    def retrieve(self, query: str, k: int = 5, rerank: bool = False) -> List[Dict[str, Any]]:
        """
        Embed query, calculate similarity, and return top-k chunks.
        Optionally rerank results (placeholder for now).
        Returns: List of dicts with keys: 'text', 'metadata', 'score', 'id'
        """
        if not query:
            return []

        # Step 1: Query Embedding
        query_embedding = self.model.encode(query, convert_to_tensor=True)
        
        # Step 2: Similarity Search
        # util.cos_sim returns a tensor of shape (1, num_docs)
        # We assume self.embeddings is a numpy array, convert to tensor implies implicit handling or explicit conversion
        # util.cos_sim works with tensors or ndarrays.
        
        # Ensure corpus_embeddings is a tensor or friendly format
        corpus_embeddings = self.embeddings
        
        # Compute cosine similarities
        hits = util.semantic_search(query_embedding, corpus_embeddings, top_k=k)
        
        # hits is a list of lists (one list per query). We have 1 query.
        query_hits = hits[0]
        
        results = []
        for hit in query_hits:
            idx = hit['corpus_id']
            score = hit['score']
            
            result = {
                'id': self.ids[idx],
                'text': self.documents[idx],
                'metadata': self.metadatas[idx],
                'score': float(score)  # Convert numpy/tensor float to native float
            }
            results.append(result)
            
        return results

    def build_context(self, retrieved_chunks: List[Dict[str, Any]]) -> str:
        """
        Assemble retrieved chunks into a single context string.
        """
        context_parts = []
        for chunk in retrieved_chunks:
            # Optional: Add clear collection/source markers if desired
            # For now, just concatenating text as requested "raw chunk text"
            context_parts.append(chunk['text'])
            
        return "\n\n".join(context_parts)

if __name__ == "__main__":
    # Basic verification
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    EMBEDDINGS_DIR = os.path.join(BASE_DIR, "phase2_vector_db")
    
    try:
        retriever = RetrievalSystem(EMBEDDINGS_DIR)
        test_query = "What are the risks of mutual funds?"
        results = retriever.retrieve(test_query, k=3)
        
        print(f"Query: {test_query}\n")
        print("Top 3 Results:")
        for res in results:
            print(f"- [Score: {res['score']:.4f}] {res['text'][:100]}...")
            
        context = retriever.build_context(results)
        print(f"\nContext Preview:\n{context[:200]}...")
        
    except Exception as e:
        print(f"Failed to initialize or retrieve: {e}")
