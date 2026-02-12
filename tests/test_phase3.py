import unittest
from unittest.mock import patch, MagicMock
import os
import sys
import numpy as np
import json
import shutil

# Ensure parent directory is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from phase3_retrieval.retrieval_pipeline import RetrievalSystem

class TestRetrievalSystem(unittest.TestCase):
    def setUp(self):
        self.embeddings_dir = "mock_embeddings_p3"
        os.makedirs(self.embeddings_dir, exist_ok=True)
        
        # Create mock artifacts
        self.documents = ["Doc 1 text about funds.", "Doc 2 text about risks.", "Doc 3 text about returns."]
        self.ids = ["id1", "id2", "id3"]
        self.metadatas = [
            {"source": "file1"}, {"source": "file2"}, {"source": "file3"}
        ]
        self.embeddings = np.array([
            [0.1, 0.2, 0.3],
            [0.4, 0.5, 0.6],
            [0.7, 0.8, 0.9]
        ], dtype=np.float32)
        
        # Save json
        with open(os.path.join(self.embeddings_dir, "vector_store.json"), 'w') as f:
            json.dump({
                "documents": self.documents,
                "ids": self.ids,
                "metadatas": self.metadatas
            }, f)
            
        # Save npy
        np.save(os.path.join(self.embeddings_dir, "embeddings.npy"), self.embeddings)

    def tearDown(self):
        if os.path.exists(self.embeddings_dir):
            shutil.rmtree(self.embeddings_dir)

    @patch('phase3_retrieval.retrieval_pipeline.SentenceTransformer')
    @patch('phase3_retrieval.retrieval_pipeline.util')
    def test_init(self, mock_util, mock_model_cls):
        retriever = RetrievalSystem(self.embeddings_dir)
        self.assertEqual(len(retriever.documents), 3)
        self.assertTrue(retriever.embeddings is not None)

    @patch('phase3_retrieval.retrieval_pipeline.SentenceTransformer')
    @patch('phase3_retrieval.retrieval_pipeline.util')
    def test_retrieve(self, mock_util, mock_model_cls):
        # Mock semantic search return
        # Format: list of lists of dicts {'corpus_id': int, 'score': float}
        mock_util.semantic_search.return_value = [[
            {'corpus_id': 1, 'score': 0.95},
            {'corpus_id': 0, 'score': 0.85}
        ]]
        
        retriever = RetrievalSystem(self.embeddings_dir)
        results = retriever.retrieve("query", k=2)
        
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]['id'], "id2") # corpus_id 1
        self.assertEqual(results[0]['score'], 0.95)
        self.assertEqual(results[1]['id'], "id1") # corpus_id 0

    @patch('phase3_retrieval.retrieval_pipeline.SentenceTransformer')
    def test_build_context(self, mock_model_cls):
        # We can test this without mocking if we pass manual dicts
        retriever = RetrievalSystem(self.embeddings_dir) # Will load mocks
        
        chunks = [
            {'text': "Hello world"},
            {'text': "Another chunk"}
        ]
        context = retriever.build_context(chunks)
        self.assertEqual(context, "Hello world\n\nAnother chunk")

if __name__ == '__main__':
    unittest.main()
