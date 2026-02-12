import streamlit as st
import os
import sys
import random

# Add project root to path for imports
# This assumes the app is run from the project root or phase_6_streamlit_app folder within the project
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.append(project_root)

# Import backend modules
try:
    from phase3_retrieval.retrieval_pipeline import RetrievalSystem
    from phase3_retrieval.query_classifier import QueryClassifier
    from phase4_generation.generation_pipeline import AnswerGenerator
    from phase4_generation.refusal_handler import RefusalHandler
    from utils.suggestions import SuggestionsHandler
except ImportError as e:
    st.error(f"Failed to import backend modules: {e}")
    st.stop()

# Page Config
st.set_page_config(
    page_title="MF Facts",
    page_icon="ℹ️",
    layout="centered"
)

# --- CSS Styling (Dark Theme matching screenshot) ---
st.markdown("""
<style>
    /* Dark background */
    .stApp {
        background-color: #1a1a1a;
    }
    
    /* Custom header */
    .custom-header {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 16px 0;
        border-bottom: 1px solid #333;
        margin-bottom: 20px;
    }
    
    .header-icon {
        width: 48px;
        height: 48px;
        background: linear-gradient(135deg, #00d4aa 0%, #00a896 100%);
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        color: #1a1a1a;
        font-weight: bold;
    }
    
    .header-text h1 {
        color: #ffffff;
        font-size: 24px;
        font-weight: 600;
        margin: 0;
        padding: 0;
    }
    
    .header-text p {
        color: #999;
        font-size: 14px;
        margin: 0;
        padding: 0;
    }
    
    /* Chat messages */
    .stChatMessage {
        background-color: transparent !important;
        padding: 8px 0 !important;
    }
    
    /* Assistant messages - left aligned, dark gray */
    [data-testid="stChatMessageContent"] {
        background-color: #2d2d2d;
        border-radius: 16px;
        padding: 14px 18px;
        color: #e0e0e0;
        max-width: 85%;
    }
    
    /* User messages - right aligned, teal */
    .stChatMessage[data-testid="user"] [data-testid="stChatMessageContent"] {
        background: linear-gradient(135deg, #00d4aa 0%, #00a896 100%);
        color: #000000;
        margin-left: auto;
    }
    
    /* Chat input */
    .stChatInput {
        background-color: #2d2d2d;
        border-radius: 24px;
    }
    
    .stChatInput input {
        background-color: #2d2d2d !important;
        color: #ffffff !important;
        border: 1px solid #444 !important;
        border-radius: 24px !important;
    }
    
    /* Remove default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1a1a1a;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #444;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #555;
    }
    
    /* Suggested questions styling */
    .suggested-questions {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-top: 15px;
    }
    
    /* Source link styling */
    .source-link {
        font-size: 12px;
        color: #00d4aa;
        margin-top: 8px;
        padding-top: 8px;
        border-top: 1px solid #444;
    }
    
    .source-link a {
        color: #00d4aa;
        text-decoration: none;
    }
    
    .source-link a:hover {
        text-decoration: underline;
    }
</style>
""", unsafe_allow_html=True)

# --- Initialization ---

@st.cache_resource
def load_rag_system():
    """Initialize Retriever and Generator only once."""
    base_dir = project_root
    embeddings_dir = os.path.join(base_dir, "phase2_vector_db")
    
    if not os.path.exists(embeddings_dir):
        st.error(f"Embeddings directory not found at {embeddings_dir}. Please run Phase 2 first.")
        st.stop()
        
    try:
        retriever = RetrievalSystem(embeddings_dir)
        classifier = QueryClassifier()
        refusal_handler = RefusalHandler()
        suggestions_handler = SuggestionsHandler()
        
        # API Key Handling: Priority st.secrets > os.getenv
        api_key = None
        if "GEMINI_API_KEY" in st.secrets:
            api_key = st.secrets["GEMINI_API_KEY"]
        
        if not api_key:
             api_key = os.getenv("GEMINI_API_KEY")
        
        if not api_key or api_key == "YOUR_GEMINI_API_KEY_HERE":
            st.error("❌ **GEMINI_API_KEY not configured!**")
            st.info("""
            **For Streamlit Cloud:**
            1. Go to your app settings
            2. Navigate to Secrets
            3. Add: `GEMINI_API_KEY = "your_actual_key"`
            
            **For Local Development:**
            1. Copy `secrets.toml.example` to `secrets.toml`
            2. Replace the placeholder with your actual API key
            """)
            st.stop()

        generator = AnswerGenerator(api_key=api_key)
        return retriever, classifier, refusal_handler, suggestions_handler, generator
    except Exception as e:
        st.error(f"❌ Failed to initialize RAG system: {type(e).__name__}")
        st.error(f"Details: {str(e)}")
        with st.expander("🔍 Full Error Trace"):
            import traceback
            st.code(traceback.format_exc())
        st.stop()

retriever, classifier, refusal_handler, suggestions_handler, generator = load_rag_system()

# Initialize Session State for Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant", 
            "content": "Hi! 👋\n\nI can help you with factual information about mutual funds using official public sources.\n\n**Facts only. No investment advice.**",
            "show_starters": True
        }
    ]

# Starter questions (fixed set)
STARTER_QUESTIONS = [
    "What is the expense ratio of HDFC Midcap Fund?",
    "Is there any exit load for HDFC Large Cap Fund?",
    "What is the minimum SIP investment required for HDFC Flexi Cap Fund?",
    "What is the risk level and benchmark of HDFC Small Cap Fund?",
    "How can I download my capital gains statement?",
]

# Alternate questions after refusal (fixed set)
ALTERNATE_QUESTIONS = [
    "What is the expense ratio of HDFC Midcap Fund?",
    "What exit load applies to HDFC Large Cap Fund?",
    "How can I download my mutual fund statements?",
]

if "show_suggestions" not in st.session_state:
    st.session_state.show_suggestions = True

# Suggested questions - verified to have answers in knowledge base
SUGGESTED_QUESTIONS = [
    "What is a Systematic Investment Plan (SIP)?",
    "What are the risks associated with mutual funds?",
    "How is NAV calculated?",
    "What are the different types of mutual funds?",
    "How can I redeem my mutual fund units?"
]

# --- UI Layout ---

# Custom Header
st.markdown("""
<div class="custom-header">
    <div class="header-icon">ℹ️</div>
    <div class="header-text">
        <h1>MF Facts</h1>
        <p>Verified mutual fund facts. No advice.</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Display Chat History
for idx, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        
        # Display source if available (only for assistant messages)
        if msg["role"] == "assistant" and "source" in msg and msg["source"]:
            source = msg["source"]
            if source.startswith("http"):
                # Get friendly display name
                from source_utils import get_source_display_name
                display_name = get_source_display_name(source)
                st.markdown(f'<div class="source-link">📎 Source: <a href="{source}" target="_blank">{display_name}</a></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="source-link">📎 Source: {source}</div>', unsafe_allow_html=True)

# Show starter questions after the first message
if st.session_state.show_suggestions and len(st.session_state.messages) == 1:
    st.markdown("<div class='suggested-questions'>", unsafe_allow_html=True)
    st.markdown("**Try asking:**")
    for idx, question in enumerate(STARTER_QUESTIONS):
        if st.button(question, key=f"starter_{idx}", use_container_width=True):
            # Trigger the question
            st.session_state.show_suggestions = False
            st.session_state.triggered_question = question
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# Handle triggered question from suggestions
if "triggered_question" in st.session_state:
    prompt = st.session_state.triggered_question
    del st.session_state.triggered_question
    # Process the triggered question immediately
else:
    prompt = None

# Always show chat input
user_input = st.chat_input("Ask a question about mutual funds...")
if user_input:
    prompt = user_input

# Handle User Input
if prompt:
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Response
    with st.chat_message("assistant"):
        with st.spinner("Analyzing documents..."):
            try:
                # 1. Check for conversational triggers
                conversational_triggers = {"ok", "okay", "thanks", "thank you", "got it", "thx", "cheers", "cool", "👍", "yes", "hi", "hello"}
                cleaned_query = "".join(char for char in prompt.lower() if char.isalnum() or char.isspace()).strip()
                
                response_text = ""
                first_source = None
                suggestions = []

                if cleaned_query in conversational_triggers:
                    response_text = "You’re welcome! 🙂 What else would you like to know about mutual funds?"
                else:
                    # 2. Query Classification
                    classification = classifier.classify(prompt)
                    
                    if classification['type'] == 'advisory':
                        # Advisory question - polite refusal
                        refusal = refusal_handler.get_refusal(prompt, classification)
                        response_text = refusal['message']
                        first_source = refusal['educational_link']
                        suggestions = refusal['suggestions']
                    else:
                        # Factual question - proceed with RAG
                        # 3. Retrieval
                        chunks = retriever.retrieve(prompt, k=5)
                        
                        # Check if we have good chunks
                        if not chunks or (chunks and chunks[0].get('score', 0) < 0.5):
                            # No answer available
                            response_text = "I don't know based on the provided sources 🙂 Try asking about specific fund details like expense ratio, SIP amount, or lock-in period."
                            first_source = None  # NO SOURCE
                            suggestions = suggestions_handler.get_no_answer_suggestions()
                        else:
                            # 4. Generation
                            response_text = generator.generate_answer(prompt, chunks)
                    
                    # 5. Source Extraction (only for factual answers with chunks)
                    if classification.get('type') == 'factual' and chunks and chunks[0].get('score', 0) >= 0.5:
                        sources = [
                            chunk.get('metadata', {}).get('source_url') or 
                            chunk.get('metadata', {}).get('source_file')
                            for chunk in chunks
                        ]
                        sources = [s for s in sources if s]
                        
                        if sources:
                            first_source = sources[0]

                # Display response
                st.markdown(response_text)
                
                # Display source below the message (if available)
                if first_source:
                    if first_source.startswith("http"):
                        from source_utils import get_source_display_name
                        display_name = get_source_display_name(first_source)
                        st.markdown(f'<div class="source-link">📎 Source: <a href="{first_source}" target="_blank">{display_name}</a></div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="source-link">📎 Source: {first_source}</div>', unsafe_allow_html=True)
                
                # Display suggestions if "I don't know"
                if suggestions:
                    st.markdown("\n\n**Try asking:**\n" + "\n".join([f"- {q}" for q in suggestions]))
                
                # Update History with source stored separately
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": response_text,
                    "source": first_source
                })
                
            except Exception as e:
                import traceback
                error_details = traceback.format_exc()
                error_msg = f"❌ Error: {type(e).__name__}: {str(e)}"
                
                # Log detailed error for debugging
                st.error(error_msg)
                with st.expander("🔍 Debug Details (click to expand)"):
                    st.code(error_details)
                
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": f"Sorry, I encountered an error. Please check:\n\n1. API key is correctly set in Streamlit Cloud Secrets\n2. All dependencies are installed\n3. Vector database files are present\n\nError: {str(e)}"
                })

