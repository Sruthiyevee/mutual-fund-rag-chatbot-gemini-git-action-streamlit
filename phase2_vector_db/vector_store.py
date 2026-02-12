import os
import json
import uuid
import numpy as np
import logging
import sqlite3
from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Phase2VectorStore:
    def __init__(self, cleaned_dir: str, embeddings_dir: str):
        self.cleaned_dir = cleaned_dir
        self.embeddings_dir = embeddings_dir
        os.makedirs(self.embeddings_dir, exist_ok=True)
        
        # Initialize Embedding Model
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # In-memory storage
        self.documents = []
        self.metadatas = []
        self.embeddings = []
        self.ids = []

    def process_all_files(self):
        """Process all JSON files in the cleaned directory."""
        if not os.path.exists(self.cleaned_dir):
            logging.error(f"Cleaned directory not found: {self.cleaned_dir}")
            return

        files = [f for f in os.listdir(self.cleaned_dir) if f.endswith('.json')]
        logging.info(f"Found {len(files)} files to process.")
        
        for filename in files:
            filepath = os.path.join(self.cleaned_dir, filename)
            self.process_file(filepath)
            
        self.save_index()
        self.save_to_sql()

    def process_file(self, filepath: str):
        """Read file, chunk text, embed, and store."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            text = data.get('extracted_text', '')
            if not text:
                logging.warning(f"No text in {filepath}")
                return

            chunks = self.create_chunks(text)
            self.store_chunks(chunks, data)
            logging.info(f"Processed {len(chunks)} chunks from {filepath}")
            
        except Exception as e:
            logging.error(f"Error processing {filepath}: {e}")

    def create_chunks(self, text: str, max_tokens: int = 400, overlap: int = 50) -> List[str]:
        """
        Split text into chunks.
        """
        words = text.split()
        
        # If text is short, return as one chunk
        if len(words) <= max_tokens:
            return [text]
            
        chunks = []
        i = 0
        step = max_tokens - overlap
        if step <= 0:
            step = 1
            
        while i < len(words):
            chunk_words = words[i : i + max_tokens]
            chunk_text = " ".join(chunk_words)
            chunks.append(chunk_text)
            i += step
            
        return chunks

    def store_chunks(self, chunks: List[str], metadata_source: Dict[str, Any]):
        """Embed and store chunks in memory."""
        if not chunks:
            return

        # Generate IDs
        new_ids = [str(uuid.uuid4()) for _ in chunks]
        
        # Prepare Metadata
        new_metadatas = []
        for _ in chunks:
            meta = {
                "scheme": metadata_source.get('scheme', 'UNKNOWN'),
                "category": metadata_source.get('category', 'UNKNOWN'),
                "source_url": metadata_source.get('source_url', ''),
                "source_type": metadata_source.get('source_type', ''),
                "source_file": metadata_source.get('source_file', '')
            }
            new_metadatas.append(meta)

        # Generate Embeddings
        new_embeddings = self.model.encode(chunks)
        
        self.documents.extend(chunks)
        self.metadatas.extend(new_metadatas)
        self.ids.extend(new_ids)
        if len(self.embeddings) == 0:
            self.embeddings = new_embeddings
        else:
            self.embeddings = np.vstack([self.embeddings, new_embeddings])

    def save_index(self):
        """Save the in-memory index to disk."""
        index_path = os.path.join(self.embeddings_dir, "vector_store.json")
        npy_path = os.path.join(self.embeddings_dir, "embeddings.npy")
        
        data = {
            "documents": self.documents,
            "metadatas": self.metadatas,
            "ids": self.ids
        }
        
        with open(index_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
            
        np.save(npy_path, self.embeddings)
        logging.info(f"Saved vector store to {self.embeddings_dir}")

    def save_to_sql(self):
        """Save embeddings and metadata to a SQLite database."""
        db_path = os.path.join(self.embeddings_dir, "embeddings.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS embeddings (
                id TEXT PRIMARY KEY,
                text_chunk TEXT,
                embedding_blob BLOB,
                scheme TEXT,
                category TEXT,
                source_url TEXT,
                source_type TEXT,
                source_file TEXT
            )
        ''')
        
        # Insert data
        for i, doc_id in enumerate(self.ids):
            embedding_bytes = self.embeddings[i].tobytes()
            meta = self.metadatas[i]
            
            cursor.execute('''
                INSERT OR REPLACE INTO embeddings (
                    id, text_chunk, embedding_blob, scheme, category, source_url, source_type, source_file
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                doc_id,
                self.documents[i],
                embedding_bytes,
                meta.get('scheme'),
                meta.get('category'),
                meta.get('source_url'),
                meta.get('source_type'),
                meta.get('source_file')
            ))
            
        conn.commit()
        conn.close()
        logging.info(f"Saved SQL database to {db_path} with {len(self.ids)} records.")

if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    PROJECT_ROOT = os.path.dirname(BASE_DIR)
    CLEANED_DIR = os.path.join(PROJECT_ROOT, "phase1_data_collection", "cleaned")
    EMBEDDINGS_DIR = BASE_DIR
    
    vector_store = Phase2VectorStore(CLEANED_DIR, EMBEDDINGS_DIR)
    vector_store.process_all_files()
