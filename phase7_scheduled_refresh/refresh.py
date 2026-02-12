import os
import sys
import logging

# Configure logging first to capture import errors if they happen later? 
# No, let's just print to stderr for debug
print(f"Current working directory: {os.getcwd()}")
print(f"Script location: {os.path.abspath(__file__)}")

# Add the project root to the python path to allow imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)
print(f"Added to sys.path: {project_root}")
print(f"sys.path: {sys.path}")

try:
    from phase1_data_collection.scraper import Phase1Scraper
except ImportError as e:
    print(f"CRITICAL ERROR: Failed to import Phase1Scraper: {e}")
    # List files in expected location
    phase1_path = os.path.join(project_root, 'phase1_data_collection')
    print(f"Checking {phase1_path}:")
    try:
        print(os.listdir(phase1_path))
    except Exception as list_e:
        print(f"Could not list directory: {list_e}")
    sys.exit(1)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - Phase7 - %(levelname)s - %(message)s')

def run_refresh():
    """
    Orchestrates the data refresh.
    Currently triggers Phase 1 scraping and cleaning.
    """
    logging.info("Starting valid scheduled data refresh...")
    
    # Define paths based on the project structure
    # We are in phase7_scheduled_refresh/refresh.py
    # Scraper expects paths relative to phase1_data_collection or absolute paths
    
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    phase1_dir = os.path.join(project_root, "phase1_data_collection")
    
    registry_path = os.path.join(phase1_dir, "resources", "resource_registry.json")
    raw_dir = os.path.join(phase1_dir, "raw")
    cleaned_dir = os.path.join(phase1_dir, "cleaned")
    
    # Validate paths
    if not os.path.exists(registry_path):
        logging.error(f"Registry not found at {registry_path}")
        sys.exit(1)
        
    logging.info(f"Using registry: {registry_path}")
    logging.info(f"Target raw directory: {raw_dir}")
    logging.info(f"Target cleaned directory: {cleaned_dir}")
    
    try:
        scraper = Phase1Scraper(registry_path, raw_dir, cleaned_dir)
        scraper.scrape_and_clean()
        logging.info("Data refresh completed successfully.")
    except Exception as e:
        logging.error(f"Data refresh failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_refresh()
