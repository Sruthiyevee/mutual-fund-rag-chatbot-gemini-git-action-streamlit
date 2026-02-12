# RAG-based Mutual Fund FAQ Chatbot

A "facts-only" chatbot that answers questions about HDFC Mutual Funds using a Retrieval-Augmented Generation (RAG) pipeline.

## Features
- **Data Scraping**: Extracts text from PDFs and HTML sources.
- **Vector Search**: Uses `sentence-transformers` and Cosine Similarity to find relevant context.
- **RAG Architecture**: Generates answers using Groq API (Llama 3), strictly grounded in retrieved facts.
- **Zero Hallucination**: Configured to refuse answering if data is missing.

## Setup

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Environment Variables**:
    
    **For CLI and Backend (`.env` file)**:
    Create a `.env` file in the root directory:
    ```
    GROQ_API_KEY=your_groq_api_key_here
    ```

    **For Streamlit App**:
    - Copy `phase_6_streamlit_app/.streamlit/secrets.toml.example` to `phase_6_streamlit_app/.streamlit/secrets.toml`
    - Replace `YOUR_GROQ_API_KEY_HERE` with your actual Groq API key
    - **Note**: `secrets.toml` is gitignored for security. Never commit API keys!

    **For Streamlit Cloud Deployment**:
    - Go to your Streamlit Cloud dashboard
    - Navigate to App Settings → Secrets
    - Add: `GROQ_API_KEY = "your_actual_key_here"`

3.  **Run the Chatbot**:
    ```bash
    python internal_chat_cli.py
    ```

## Project Structure

- **`phase1_data_collection/`**: Scraper logic and data storage (`raw/`, `cleaned/`).
- **`phase2_vector_db/`**: Vector store logic and artifacts (`embeddings.db`, `vector_store.json`).
- **`phase3_retrieval/`**: Retrieval pipeline logic.
- **`phase4_generation/`**: LLM generation logic.
- **`tests/`**: Unit tests.

## Testing
Run all unit tests:
```bash
python -m unittest discover tests
```
