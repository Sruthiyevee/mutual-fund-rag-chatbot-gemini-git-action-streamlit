import unittest
from unittest.mock import patch, MagicMock
import os
import shutil
import sys
import json
import sqlite3
import numpy as np

# Ensure parent directory is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from phase2_vector_db.vector_store import Phase2VectorStore

class TestPhase2VectorStore(unittest.TestCase):
    def setUp(self):
        self.cleaned_dir = "mock_cleaned_p2"
        self.embeddings_dir = "mock_embeddings_p2"
        os.makedirs(self.cleaned_dir, exist_ok=True)
        os.makedirs(self.embeddings_dir, exist_ok=True)
        
        # Create a dummy JSON file
        self.dummy_data = {
            "scheme": "Test Scheme",
            "category": "Test Category",
            "extracted_text": "Word " * 100, 
            "source_url": "http://example.com"
        }
        with open(os.path.join(self.cleaned_dir, "test.json"), 'w') as f:
            json.dump(self.dummy_data, f)

    def tearDown(self):
        if os.path.exists(self.cleaned_dir):
            shutil.rmtree(self.cleaned_dir)
        if os.path.exists(self.embeddings_dir):
            shutil.rmtree(self.embeddings_dir)

    @patch('phase2_vector_db.vector_store.SentenceTransformer')
    def test_init(self, mock_model):
        store = Phase2VectorStore(self.cleaned_dir, self.embeddings_dir)
        mock_model.assert_called_with('all-MiniLM-L6-v2')
        self.assertEqual(store.documents, [])

    def test_create_chunks(self):
        with patch('phase2_vector_db.vector_store.SentenceTransformer'):
            store = Phase2VectorStore(self.cleaned_dir, self.embeddings_dir)
            text = "Word " * 50
            chunks = store.create_chunks(text, max_tokens=10, overlap=0)
            self.assertTrue(len(chunks) > 1)
            
            short_text = "Just a few words."
            chunks = store.create_chunks(short_text)
            self.assertEqual(len(chunks), 1)

    @patch('phase2_vector_db.vector_store.SentenceTransformer')
    def test_process_file_and_save(self, mock_model):
        # Mock embedding return
        mock_model_instance = mock_model.return_value
        # return a numpy array for embeddings
        mock_model_instance.encode.return_value = np.array([[0.1]*384] * 5) # 5 chunks

        store = Phase2VectorStore(self.cleaned_dir, self.embeddings_dir)
        
        # We need to ensure chunking produces something, so we rely on real chunking logic
        # process_file calls create_chunks then store_chunks
        store.process_file(os.path.join(self.cleaned_dir, "test.json"))
        
        self.assertTrue(len(store.documents) > 0)
        self.assertTrue(len(store.metadatas) > 0)
        
        # Test Save
        store.save_index()
        self.assertTrue(os.path.exists(os.path.join(self.embeddings_dir, "vector_store.json")))
        self.assertTrue(os.path.exists(os.path.join(self.embeddings_dir, "embeddings.npy")))
        
        # Test SQL Save
        store.save_to_sql()
        db_path = os.path.join(self.embeddings_dir, "embeddings.db")
        self.assertTrue(os.path.exists(db_path))
        
        # Verify SQL content
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM embeddings")
        count = cursor.fetchone()[0]
        conn.close()
        self.assertTrue(count > 0)

if __name__ == '__main__':
    unittest.main()
