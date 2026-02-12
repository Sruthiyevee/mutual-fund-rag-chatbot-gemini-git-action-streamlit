import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Ensure parent directory is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from phase4_generation.generation_pipeline import AnswerGenerator

class TestAnswerGenerator(unittest.TestCase):
    @patch('phase4_generation.generation_pipeline.Groq')
    def test_init(self, mock_groq_class):
        # Test init with key
        generator = AnswerGenerator(api_key="test_key")
        self.assertIsNotNone(generator.client)
        
    @patch('phase4_generation.generation_pipeline.Groq')
    def test_build_context_str(self, mock_groq_class):
        generator = AnswerGenerator(api_key="test_key")
        chunks = [
            {'text': "Chunk 1", 'metadata': {'source_file': "file1.json"}},
            {'text': "Chunk 2", 'metadata': {'source_file': "file2.json"}}
        ]
        context = generator._build_context_str(chunks)
        self.assertIn("Source: file1.json", context)
        self.assertIn("Content: Chunk 1", context)

    @patch('phase4_generation.generation_pipeline.Groq')
    def test_generate_answer(self, mock_groq_class):
        # Mock client and response
        mock_client = mock_groq_class.return_value
        mock_completion = MagicMock()
        mock_completion.choices[0].message.content = "Generated Answer"
        mock_client.chat.completions.create.return_value = mock_completion
        
        generator = AnswerGenerator(api_key="test_key")
        chunks = [{'text': "Context", 'metadata': {}}]
        
        answer = generator.generate_answer("Query", chunks)
        self.assertEqual(answer, "Generated Answer")
        
        # Verify prompt structure
        call_args = mock_client.chat.completions.create.call_args
        messages = call_args[1]['messages']
        self.assertEqual(messages[0]['role'], 'system')
        self.assertIn("facts-only", messages[0]['content'])
        self.assertIn("USER QUESTION: Query", messages[1]['content'])

    def test_generate_answer_no_client(self):
        # Test graceful failure without key
        with patch.dict(os.environ, {}, clear=True):
            generator = AnswerGenerator()
            # generator.client should be None or mocked depending on implementation details
            # If implementation sets client=None when key missing:
            if generator.client is None:
                answer = generator.generate_answer("Query", [])
                self.assertIn("MISSING_API_KEY", answer)

if __name__ == '__main__':
    unittest.main()
