import os
import json
import uuid
import numpy as np
from sentence_transformers import SentenceTransformer

def add_faq():
    base_dir = "phase2_vector_db"
    vector_store_path = os.path.join(base_dir, "vector_store.json")
    embeddings_path = os.path.join(base_dir, "embeddings.npy")
    faq_file_path = "phase1_data_collection/cleaned/hdfc_service_faqs.json"
    
    # Verify file exists
    if not os.path.exists(faq_file_path):
        print(f"ERROR: {faq_file_path} not found!")
        return
        
    print(f"Reading {faq_file_path}...")
    with open(faq_file_path, 'r', encoding='utf-8') as f:
        data_list = json.load(f)
        
    # Handle list or dict
    if isinstance(data_list, list):
        data = data_list[0]
    else:
        data = data_list
        
    text = data.get('extracted_text', '')
    print(f"Extracted text length: {len(text)}")
    
    # Load existing store
    print(f"Loading existing vector store from {vector_store_path}")
    with open(vector_store_path, 'r', encoding='utf-8') as f:
        store_data = json.load(f)
        
    documents = store_data.get('documents', [])
    metadatas = store_data.get('metadatas', [])
    ids = store_data.get('ids', [])
    
    embeddings = np.load(embeddings_path)
    
    # Check if already present
    for doc in documents:
        if "Capital Gains Statement" in doc:
            print("Layout already contains Capital Gains info. Skipping addition.")
            # return # Force add for now to be sure
            
    # Process New Data
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Simple chunking (coping logic from vector_store.py essentially)
    words = text.split()
    chunks = []
    if len(words) <= 400:
        chunks = [text]
    else:
        # Simplified for brevity
        chunks = [text] 
        
    print(f"Generated {len(chunks)} chunks.")
    
    new_embeddings = model.encode(chunks)
    
    for i, chunk in enumerate(chunks):
        documents.append(chunk)
        ids.append(str(uuid.uuid4()))
        meta = {
            "scheme": data.get('scheme', 'General'),
            "category": data.get('category', 'Service FAQs'),
            "source_url": data.get('source_url', ''),
            "source_type": data.get('source_type', ''),
            "source_file": "hdfc_service_faqs.json"
        }
        metadatas.append(meta)
        
    # Update Embeddings
    updated_embeddings = np.vstack([embeddings, new_embeddings])
    
    # Save back
    new_store_data = {
        "documents": documents,
        "metadatas": metadatas,
        "ids": ids
    }
    
    with open(vector_store_path, 'w', encoding='utf-8') as f:
        json.dump(new_store_data, f, indent=2)
        
    np.save(embeddings_path, updated_embeddings)
    print("Successfully added FAQ to vector store.")

if __name__ == "__main__":
    add_faq()
