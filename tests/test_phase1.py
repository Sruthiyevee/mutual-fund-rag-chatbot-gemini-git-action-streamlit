import unittest
from unittest.mock import patch, MagicMock, mock_open
import os
import json
import io
import sys

# Ensure the parent directory is in the path to import the scraper
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from phase1_data_collection.scraper import Phase1Scraper

class TestPhase1Scraper(unittest.TestCase):
    def setUp(self):
        self.registry_path = "mock_registry.json"
        self.raw_dir = "mock_raw"
        self.cleaned_dir = "mock_cleaned"
        
        # Create a dummy registry file
        self.registry_data = [
            {
                "resource_name": "Test PDF",
                "source": "Test Source",
                "scheme": "Test Scheme",
                "document_type": "SID",
                "url": "http://example.com/test.pdf"
            },
            {
                "resource_name": "Test HTML",
                "source": "Test Source",
                "scheme": "COMMON",
                "document_type": "Educational",
                "url": "http://example.com/test.html"
            }
        ]
        with open(self.registry_path, 'w') as f:
            json.dump(self.registry_data, f)
            
    def tearDown(self):
        if os.path.exists(self.registry_path):
            os.remove(self.registry_path)
        if os.path.exists(self.raw_dir):
            import shutil
            shutil.rmtree(self.raw_dir)
        if os.path.exists(self.cleaned_dir):
            shutil.rmtree(self.cleaned_dir)

    @patch('os.makedirs')
    def test_init(self, mock_makedirs):
        scraper = Phase1Scraper(self.registry_path, self.raw_dir, self.cleaned_dir)
        self.assertEqual(scraper.raw_dir, self.raw_dir)
        mock_makedirs.assert_any_call(self.raw_dir, exist_ok=True)
        
    @patch('requests.get')
    def test_extract_html(self, mock_get):
        mock_response = MagicMock()
        mock_response.text = "<html><body><p>Hello World</p><script>alert('hi')</script></body></html>"
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        scraper = Phase1Scraper(self.registry_path, self.raw_dir, self.cleaned_dir)
        text = scraper.extract_text_from_html("http://example.com")
        self.assertIn("Hello World", text)
        self.assertNotIn("alert", text)

    def test_clean_text(self):
        scraper = Phase1Scraper(self.registry_path, self.raw_dir, self.cleaned_dir)
        dirty_text = "  This   is  a   test.  \n New line. "
        cleaned = scraper.clean_text(dirty_text, "Test Source")
        self.assertEqual(cleaned, "This is a test. New line.")

    @patch('phase1_data_collection.scraper.Phase1Scraper.save_json')
    @patch('phase1_data_collection.scraper.Phase1Scraper.extract_text_from_html')
    def test_process_resource(self, mock_extract, mock_save):
        mock_extract.return_value = "Extracted Text"
        scraper = Phase1Scraper(self.registry_path, self.raw_dir, self.cleaned_dir)
        
        resource = self.registry_data[1] # HTML resource
        scraper.process_resource(resource)
        
        self.assertEqual(mock_save.call_count, 2) # Raw and Cleaned
        
    @patch('requests.get')
    @patch('pypdf.PdfReader')
    def test_extract_pdf(self, mock_pdf_reader, mock_get):
        # Mocking PDF extraction is tricky without a real file file-like object, 
        # but we can mock the PdfReader behavior.
        mock_response = MagicMock()
        mock_response.content = b"%PDF-1.4..."
        mock_get.return_value = mock_response
        
        mock_page = MagicMock()
        mock_page.extract_text.return_value = "PDF Page Text"
        
        mock_pdf_instance = MagicMock()
        mock_pdf_instance.pages = [mock_page]
        mock_pdf_reader.return_value = mock_pdf_instance
        
        scraper = Phase1Scraper(self.registry_path, self.raw_dir, self.cleaned_dir)
        text = scraper.extract_text_from_pdf("http://example.com/test.pdf")
        
        self.assertIn("PDF Page Text", text)

if __name__ == '__main__':
    unittest.main()
