import os
import json
import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import logging
from typing import Dict, Any, Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Phase1Scraper:
    def __init__(self, resource_registry_path: str, raw_dir: str, cleaned_dir: str):
        self.resource_registry_path = resource_registry_path
        self.raw_dir = raw_dir
        self.cleaned_dir = cleaned_dir
        
        # Create directories if they don't exist
        os.makedirs(self.raw_dir, exist_ok=True)
        os.makedirs(self.cleaned_dir, exist_ok=True)
        
        # Load registry
        with open(self.resource_registry_path, 'r') as f:
            self.registry = json.load(f)

    def scrape_and_clean(self):
        """Main method to iterate through resources and process them."""
        for resource in self.registry:
            try:
                self.process_resource(resource)
            except Exception as e:
                logging.error(f"Failed to process resource {resource.get('resource_name')}: {e}")

    def process_resource(self, resource: Dict[str, Any]):
        """Process a single resource: fetch, extract, clean, and save."""
        url = resource.get('url')
        resource_name = resource.get('resource_name')
        source_type = resource.get('source')
        doc_type = resource.get('document_type')
        scheme = resource.get('scheme', 'COMMON')
        
        logging.info(f"Processing: {resource_name}")
        
        raw_text = ""
        
        if url.lower().endswith('.pdf'):
            raw_text = self.extract_text_from_pdf(url)
        else:
            raw_text = self.extract_text_from_html(url)
            
        if not raw_text:
            logging.warning(f"No text extracted for {resource_name}")
            return

        # Save Raw Data
        raw_filename = self.get_filename(resource_name, "raw")
        raw_entry = {
            "scheme": scheme,
            "category": doc_type,
            "raw_text": raw_text,
            "source_url": url,
            "source_type": source_type
        }
        self.save_json(raw_entry, os.path.join(self.raw_dir, raw_filename))
        
        # Clean Data
        cleaned_text = self.clean_text(raw_text, source_type)
        
        # Save Cleaned Data
        cleaned_filename = self.get_filename(resource_name, "cleaned")
        cleaned_entry = {
            "scheme": scheme,
            "category": doc_type,
            "extracted_text": cleaned_text,
            "source_url": url,
            "source_type": source_type
        }
        self.save_json(cleaned_entry, os.path.join(self.cleaned_dir, cleaned_filename))
        logging.info(f"Successfully processed {resource_name}")

    def extract_text_from_pdf(self, url: str) -> str:
        """Download and extract text from PDF."""
        try:
            # For this phase, we assume we might need to download or use local.
            # If local_file_path is null, we download to a temp location or memory.
            # Using pypdf for extraction.
            # Check if we should use a local file if available in registry (not implemented in registry yet properly)
            
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            # Save properly to a temp file or process in memory if possible, 
            # but pypdf usually likes files.
            import io
            from pypdf import PdfReader
            
            remote_file = io.BytesIO(response.content)
            reader = PdfReader(remote_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            logging.error(f"Error extracting PDF from {url}: {e}")
            return ""

    def extract_text_from_html(self, url: str) -> str:
        """Extract text from HTML."""
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.decompose()
                
            text = soup.get_text()
            return text
        except Exception as e:
            logging.error(f"Error extracting HTML from {url}: {e}")
            return ""

    def clean_text(self, text: str, source_type: str) -> str:
        """Clean and normalize extracted text."""
        # collapse white spaces
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Specific cleaning rules can be added here
        # For now, we perform basic normalization
        
        return text

    def get_filename(self, resource_name: str, type_suffix: str) -> str:
        """Generate a filename from resource name."""
        clean_name = re.sub(r'[^\w\-_\. ]', '_', resource_name)
        return f"{clean_name.replace(' ', '_').lower()}_{type_suffix}.json"

    def save_json(self, data: Dict, filepath: str):
        """Save data to JSON file."""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    # Define paths
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    REGISTRY_PATH = os.path.join(BASE_DIR, "resources", "resource_registry.json")
    RAW_DIR = os.path.join(BASE_DIR, "raw")
    CLEANED_DIR = os.path.join(BASE_DIR, "cleaned")
    
    scraper = Phase1Scraper(REGISTRY_PATH, RAW_DIR, CLEANED_DIR)
    scraper.scrape_and_clean()
