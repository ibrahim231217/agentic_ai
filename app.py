"""
Agentic AI Document Assistant - Main Streamlit Application
Phase 1: API Integration and Agent Introduction

This is a simple web application that allows users to:
1. Upload documents (PDF, DOCX, TXT)
2. Select processing agents
3. View generated outputs
4. Download results

Technology Stack:
- Frontend: Streamlit
- Backend: Python with multiple AI agents
- APIs: OpenRouter (for Document and Information agents) and Gemini (for Summary agent)
"""

import streamlit as st
import os
import tempfile
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Import agents and utilities
from agents.document_agent import DocumentAgent
from agents.summary_agent import SummaryAgent
from agents.info_agent import InfoAgent
from utils.file_handler import extract_text, save_text_to_file, validate_file

# Load environment variables
load_dotenv()

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Agentic AI Document Assistant",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM STYLING
# ============================================================================

st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #0066cc;
        color: white;
    }
    .stButton>button:hover {
        background-color: #0052a3;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 12px;
        border-radius: 4px;
        margin: 10px 0;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 12px;
        border-radius: 4px;
        margin: 10px 0;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
        padding: 12px;
        border-radius: 4px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

def initialize_session_state():
    """Initialize session state variables."""
    if "uploaded_file" not in st.session_state:
        st.session_state.uploaded_file = None
    
    if "document_text" not in st.session_state:
        st.session_state.document_text = ""
    
    if "filename" not in st.session_state:
        st.session_state.filename = ""
    
    if "input_text" not in st.session_state:
        st.session_state.input_text = ""
    
    if "results" not in st.session_state:
        st.session_state.results = {
            "document_agent": None,
            "summary_agent": None,
            "info_agent": None
        }
    
    if "processing" not in st.session_state:
        st.session_state.processing = False


initialize_session_state()

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def check_api_keys() -> bool:
    """Check if required API keys are configured."""
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    gemini_key = os.getenv("GEMINI_API_KEY")
    
    if not openrouter_key:
        st.error("❌ **OPENROUTER_API_KEY** not found. Please set it in your .env file.")
        return False
    
    if not gemini_key:
        st.warning("⚠️ **GEMINI_API_KEY** not found. Summarization will fallback to OpenRouter.")
    
    return True


def process_document(file_content, filename: str) -> bool:
    """
    Process uploaded document and extract text.
    
    Args:
        file_content: Uploaded file content
        filename: Name of the file
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Save uploaded file to temporary location
        temp_file_path = os.path.join("uploads", filename)
        os.makedirs("uploads", exist_ok=True)
        
        with open(temp_file_path, "wb") as f:
            f.write(file_content)
        
        # Validate file
        is_valid, message = validate_file(temp_file_path)
        
        if not is_valid:
            st.error(f"❌ File validation failed: {message}")
            return False
        
        # Extract text from document
        text = extract_text(temp_file_path)
        
        if not text or len(text.strip()) == 0:
            st.error("❌ Could not extract text from document. Please check the file format.")
            return False
        
        # Update session state
        st.session_state.document_text = text
        st.session_state.filename = filename
        st.session_state.uploaded_file = temp_file_path
        
        # Clean up
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        
        st.success(f"✅ Document loaded successfully! ({len(text)} characters)")
        return True
    
    except Exception as e:
        st.error(f"❌ Error processing document: {str(e)}")
        return False


def run_document_agent() -> bool:
    """Run the Document Agent."""
    try:
        with st.spinner("🔄 Document Agent processing... This may take a moment."):
            agent = DocumentAgent()
            result = agent.process_document(st.session_state.document_text)
            
            if result["status"] == "success":
                st.session_state.results["document_agent"] = result
                st.success("✅ Document Agent completed successfully!")
                return True
            else:
                st.error(f"❌ Document Agent error: {result.get('message', 'Unknown error')}")
                return False
    
    except Exception as e:
        st.error(f"❌ Error running Document Agent: {str(e)}")
        return False


def run_summary_agent() -> bool:
    """Run the Summary Agent."""
    try:
        with st.spinner("🔄 Summary Agent processing... This may take a moment."):
            agent = SummaryAgent()
            result = agent.process_document(st.session_state.document_text)
            
            if result["status"] == "success":
                st.session_state.results["summary_agent"] = result
                st.success(f"✅ Summary Agent completed successfully! (API: {result.get('api_used', 'unknown')})")
                return True
            else:
                st.error(f"❌ Summary Agent error: {result.get('message', 'Unknown error')}")
                return False
    
    except Exception as e:
        st.error(f"❌ Error running Summary Agent: {str(e)}")
        return False


def run_info_agent() -> bool:
    """Run the Information Agent."""
    try:
        with st.spinner("🔄 Information Agent processing... This may take a moment."):
            agent = InfoAgent()
            result = agent.process_document(st.session_state.document_text)
            
            if result["status"] == "success":
                st.session_state.results["info_agent"] = result
                st.success("✅ Information Agent completed successfully!")
                return True
            else:
                st.error(f"❌ Information Agent error: {result.get('message', 'Unknown error')}")
                return False
    
    except Exception as e:
        st.error(f"❌ Error running Information Agent: {str(e)}")
        return False


def create_download_file(content: str, file_type: str) -> bytes:
    """
    Create a downloadable file.
    
    Args:
        content: File content
        file_type: Type of file (document, summary, info, report)
        
    Returns:
        File content as bytes
    """
    return content.encode('utf-8')


def run_all_agents() -> None:
    """Run all agents sequentially and keep results in session state."""
    if not st.session_state.document_text:
        st.error("❌ No document text found to process.")
        return

    st.session_state.results = {
        "document_agent": None,
        "summary_agent": None,
        "info_agent": None
    }

    run_document_agent()
    run_summary_agent()
    run_info_agent()


# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    # Header
    st.title("📄 Agentic AI Document Assistant")
    st.markdown("### Phase 1: API Integration and Agent Introduction")
    st.markdown("---")
    
    # Check API keys
    if not check_api_keys():
        st.stop()
    
    # Sidebar - Information
    with st.sidebar:
        st.header("📋 About")
        st.markdown("""
        This application demonstrates multiple AI agents working together:
        
        **Agent 1: Document Checking**
        - Grammar and clarity review
        - Professional rewriting
        - Document enhancement
        
        **Agent 2: Summarization**
        - Executive summaries
        - Key points extraction
        - Takeaways
        
        **Agent 3: Information Extraction**
        - Entity identification
        - Action items
        - Data point extraction
        - Distribution reports
        """)
        
        st.markdown("---")
        st.markdown("**Powered by:**")
        st.markdown("- 🔗 OpenRouter (Document & Info Agents)")
        st.markdown("- 🤖 Gemini (Summary Agent)")
        
        st.markdown("---")
        st.markdown("""
        **Free API Resources:**
        - [OpenRouter](https://openrouter.ai)
        - [Google AI Studio](https://ai.google.dev/)
        """)
    
    # Main content area
    st.header("📤 Upload a document or paste text")

    uploaded_file = st.file_uploader(
        "Upload a PDF, DOCX, or TXT file, or leave empty to paste text below",
        type=["pdf", "docx", "txt"],
        help="Upload a document or paste raw text in the box below."
    )

    st.session_state.input_text = st.text_area(
        "Paste raw text here:",
        st.session_state.input_text,
        height=220,
        placeholder="Paste text here if not uploading a document..."
    )

    if st.button("Process Document", use_container_width=True):
        if uploaded_file is not None:
            if process_document(uploaded_file.getvalue(), uploaded_file.name):
                st.session_state.input_text = ""
                run_all_agents()
        elif st.session_state.input_text and st.session_state.input_text.strip():
            st.session_state.document_text = st.session_state.input_text.strip()
            st.session_state.filename = "manual_text"
            st.success(f"✅ Text loaded successfully! ({len(st.session_state.document_text)} characters)")
            run_all_agents()
        else:
            st.error("❌ Please upload a document or paste some text before processing.")

    if st.session_state.document_text:
        st.markdown("---")
        st.subheader("📖 Document Preview")
        preview_length = min(500, len(st.session_state.document_text))
        st.text_area(
            "Preview (first 500 characters):",
            st.session_state.document_text[:preview_length],
            height=150,
            disabled=True
        )
        st.caption(f"Total document length: {len(st.session_state.document_text)} characters")

    if any(st.session_state.results.values()):
                st.markdown("---")
                st.header("📋 Step 3: Results")
                
                # Document Agent Results
                if st.session_state.results["document_agent"]:
                    with st.expander("✍️ Document Agent - Improved Document", expanded=True):
                        result = st.session_state.results["document_agent"]
                        
                        if result["status"] == "success":
                            st.markdown("**Improved Document:**")
                            st.text_area(
                                "Improved version:",
                                result.get("improved_document", ""),
                                height=250,
                                disabled=True,
                                key="improved_doc"
                            )
                            
                            st.markdown("**Changes Summary:**")
                            st.info(result.get("changes_summary", ""))
                            
                            # Download button
                            download_content = f"""IMPROVED DOCUMENT
=====================================

{result.get('improved_document', '')}

CHANGES SUMMARY
=====================================
{result.get('changes_summary', '')}

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
                            st.download_button(
                                label="⬇️ Download Improved Document",
                                data=create_download_file(download_content, "document"),
                                file_name=f"improved_{st.session_state.filename}.txt",
                                mime="text/plain",
                                key="download_doc_agent"
                            )
                        else:
                            st.error(result.get("message", "Error processing document"))
                
                # Summary Agent Results
                if st.session_state.results["summary_agent"]:
                    with st.expander("📊 Summary Agent - Document Summary", expanded=True):
                        result = st.session_state.results["summary_agent"]
                        
                        if result["status"] == "success":
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.markdown("**Executive Summary:**")
                                st.info(result.get("executive_summary", ""))
                            
                            with col2:
                                st.markdown("**API Used:**")
                                st.info(f"🔗 {result.get('api_used', 'unknown').upper()}")
                            
                            st.markdown("**Bullet-Point Summary:**")
                            st.text_area(
                                "Bullet points:",
                                result.get("bullet_summary", ""),
                                height=150,
                                disabled=True,
                                key="bullet_summary"
                            )
                            
                            st.markdown("**Key Takeaways:**")
                            st.text_area(
                                "Key takeaways:",
                                result.get("key_takeaways", ""),
                                height=150,
                                disabled=True,
                                key="key_takeaways"
                            )
                            
                            # Download button
                            download_content = f"""DOCUMENT SUMMARY
=====================================

EXECUTIVE SUMMARY
{result.get('executive_summary', '')}

BULLET-POINT SUMMARY
{result.get('bullet_summary', '')}

KEY TAKEAWAYS
{result.get('key_takeaways', '')}

API Used: {result.get('api_used', 'unknown')}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
                            st.download_button(
                                label="⬇️ Download Summary",
                                data=create_download_file(download_content, "summary"),
                                file_name=f"summary_{st.session_state.filename}.txt",
                                mime="text/plain",
                                key="download_summary_agent"
                            )
                        else:
                            st.error(result.get("message", "Error generating summary"))
                
                # Information Agent Results
                if st.session_state.results["info_agent"]:
                    with st.expander("📈 Information Agent - Extracted Information", expanded=True):
                        result = st.session_state.results["info_agent"]
                        
                        if result["status"] == "success":
                            st.markdown("**Important Entities:**")
                            st.text_area(
                                "Entities:",
                                result.get("entities", ""),
                                height=120,
                                disabled=True,
                                key="entities"
                            )
                            
                            st.markdown("**Action Items:**")
                            st.text_area(
                                "Action items:",
                                result.get("action_items", ""),
                                height=120,
                                disabled=True,
                                key="action_items"
                            )
                            
                            st.markdown("**Key Data Points:**")
                            st.text_area(
                                "Data points:",
                                result.get("data_points", ""),
                                height=120,
                                disabled=True,
                                key="data_points"
                            )
                            
                            st.markdown("**Categorized Information:**")
                            st.text_area(
                                "Categorized info:",
                                result.get("categorized_info", ""),
                                height=120,
                                disabled=True,
                                key="categorized_info"
                            )
                            
                            st.markdown("**Distribution-Ready Report:**")
                            st.text_area(
                                "Report:",
                                result.get("distribution_report", ""),
                                height=150,
                                disabled=True,
                                key="distribution_report"
                            )
                            
                            # Download button
                            download_content = f"""INFORMATION EXTRACTION REPORT
=====================================

IMPORTANT ENTITIES
{result.get('entities', '')}

ACTION ITEMS
{result.get('action_items', '')}

KEY DATA POINTS
{result.get('data_points', '')}

CATEGORIZED INFORMATION
{result.get('categorized_info', '')}

DISTRIBUTION-READY REPORT
{result.get('distribution_report', '')}

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
                            st.download_button(
                                label="⬇️ Download Information Report",
                                data=create_download_file(download_content, "info"),
                                file_name=f"info_report_{st.session_state.filename}.txt",
                                mime="text/plain",
                                key="download_info_agent"
                            )
                        else:
                            st.error(result.get("message", "Error extracting information"))
                
                # Download Combined Report
                st.markdown("---")
                st.header("📥 Step 4: Download Results")
                
                if all(st.session_state.results.values()):
                    st.subheader("Complete Analysis Report")
                    
                    report_content = f"""AGENTIC AI DOCUMENT ANALYSIS REPORT
=====================================
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Document: {st.session_state.filename}

════════════════════════════════════════════════════════════

1. DOCUMENT IMPROVEMENT (Document Agent)
────────────────────────────────────────

IMPROVED DOCUMENT:
{st.session_state.results['document_agent'].get('improved_document', 'N/A')}

CHANGES MADE:
{st.session_state.results['document_agent'].get('changes_summary', 'N/A')}

════════════════════════════════════════════════════════════

2. DOCUMENT SUMMARY (Summary Agent)
────────────────────────────────────────

EXECUTIVE SUMMARY:
{st.session_state.results['summary_agent'].get('executive_summary', 'N/A')}

BULLET POINTS:
{st.session_state.results['summary_agent'].get('bullet_summary', 'N/A')}

KEY TAKEAWAYS:
{st.session_state.results['summary_agent'].get('key_takeaways', 'N/A')}

════════════════════════════════════════════════════════════

3. INFORMATION EXTRACTION (Information Agent)
────────────────────────────────────────────

ENTITIES:
{st.session_state.results['info_agent'].get('entities', 'N/A')}

ACTION ITEMS:
{st.session_state.results['info_agent'].get('action_items', 'N/A')}

DATA POINTS:
{st.session_state.results['info_agent'].get('data_points', 'N/A')}

CATEGORIZED INFORMATION:
{st.session_state.results['info_agent'].get('categorized_info', 'N/A')}

DISTRIBUTION REPORT:
{st.session_state.results['info_agent'].get('distribution_report', 'N/A')}

════════════════════════════════════════════════════════════
End of Report
"""
                    
                    st.download_button(
                        label="⬇️ Download Complete Report (All Agents)",
                        data=create_download_file(report_content, "complete"),
                        file_name=f"complete_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain",
                        key="download_complete_report"
                    )
                else:
                    st.info("Run all three agents to generate the complete report.")


if __name__ == "__main__":
    main()
