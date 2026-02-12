# 🤖 Mutual Fund RAG Chatbot

A **facts-only** AI assistant that answers questions about HDFC Mutual Funds using Retrieval-Augmented Generation (RAG). It strictly provides factual information from official Schema Information Documents (SIDs), Key Information Memorandums (KIMs), and website content, ensuring **zero hallucinations** and **no investment advice**.

---

## 📋 Scope

### ✅ What it Covers
*   **Funds**:
    *   HDFC Midcap Opportunities Fund
    *   HDFC Flexi Cap Fund
    *   HDFC Small Cap Fund
    *   HDFC Multi Cap Fund
    *   HDFC Top 100 Fund (Large Cap)
*   **Documents**:
    *   Official SIDs and KIMs (PDFs)
    *   Monthly Factsheets
    *   Official Fund Website Pages
*   **Topics**:
    *   Expense Ratios, Exit Loads, Lock-in periods
    *   Min SIP/Lumpsum amounts
    *   Riskometers and Benchmarks
    *   Fund Managers and Investment Strategy

### ❌ What it Does NOT Do
*   **No Advice**: Will strictly refuse to recommend funds or predict future returns.
*   **No Live Data**: NAVs and returns are based on the latest scraped data (refreshed weekly), not real-time market feeds.
*   **No Comparisons**: Does not compare performance against other AMCs.

---

## ⚡ Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Sruthiyevee/mutual-fund-rag-chatbot-gemini-git-action-streamlit.git
cd mutual-fund-rag-chatbot-gemini-git-action-streamlit
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure API Keys
This project uses **Groq** for fast, cost-effective inference.

**For Local Run:**
Create a `.env` file in the root directory:
```bash
GROQ_API_KEY=your_groq_api_key_here
```

**For Streamlit App (Local):**
Create `.streamlit/secrets.toml` inside `phase_6_streamlit_app/`:
```toml
GROQ_API_KEY = "your_groq_api_key_here"
```

---

## 🚀 Running the App

### Option 1: Web Interface (Streamlit)
The primary interface with a dark-themed UI.
```bash
streamlit run phase_6_streamlit_app/app.py
```

### Option 2: Command Line Interface (CLI)
For quick testing and debugging.
```bash
python internal_chat_cli.py
```

---

## ☁️ Deployment (Streamlit Cloud)

1.  **Push to GitHub**: Ensure your latest code is on the `main` branch.
2.  **New App**: Go to [share.streamlit.io](https://share.streamlit.io/) and create a new app.
3.  **Select Repository**: Choose this repo and set the **Main file path** to:
    `phase_6_streamlit_app/app.py`
4.  **Add Secrets**: In the Advanced Settings, add your API key:
    ```toml
    GROQ_API_KEY = "your_actual_api_key"
    ```
5.  **Deploy**: Click "Deploy"!

---

## ⚠️ Known Limits

1.  **Data Latency**: Data is updated via a scheduled GitHub Action weekly. Recent changes (last 1-6 days) may not be reflected immediately.
2.  **Context Limit**: The system retrieves the top 5 most relevant chunks. Complex questions requiring synthesis of 10+ documents may have partial answers.
3.  **Table parsing**: While PDF text is extracted, complex nested tables in SIDs might potentially lose some structural fidelity in the text-only conversion.

---

## 🏗️ Architecture
For a deep dive into the 7-phase architecture, scraper logic, and vector database design, please see [**architecture_design.md**](architecture_design.md).
