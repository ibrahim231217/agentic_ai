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
from datetime import datetime
from dotenv import load_dotenv

# Import agents and utilities
from agents.document_agent import DocumentAgent
from agents.summary_agent import SummaryAgent
from agents.info_agent import InfoAgent
from utils.file_handler import extract_text, validate_file

# Load environment variables
load_dotenv()

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Agentic AI Document Assistant",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM STYLING
# ============================================================================

st.markdown("""
    <style>
    body, .stApp, .main {
        background-color: #080808;
        color: #f7f7f7;
        font-family: 'Inter', sans-serif;
    }

    .app-shell {
        background: transparent;
    }

    .section-card {
        background: #111111;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 24px;
        padding: 26px;
        margin-bottom: 22px;
    }

    .section-header {
        color: #ffffff;
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 0.35rem;
    }

    .section-subtitle {
        color: #b3b3b3;
        font-size: 1rem;
        line-height: 1.7;
        margin-bottom: 1.4rem;
    }

    .result-card {
        background: #141414;
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 22px;
        padding: 20px;
        margin-top: 18px;
    }

    .result-header {
        color: #ffffff;
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 15px;
    }

    .secondary-text {
        color: #9ca3af;
        margin-bottom: 4px;
    }

    .stButton>button,
    .stDownloadButton>button {
        width: 100%;
        background-color: #c8102e;
        color: #ffffff;
        border: none;
        border-radius: 999px;
        padding: 0.95rem 1.3rem;
        font-weight: 700;
        font-size: 1rem;
    }

    .stButton>button:hover,
    .stDownloadButton>button:hover {
        background-color: #a10a24;
    }

    .stTextArea>div>div>textarea {
        background: #0f0f0f;
        color: #f7f7f7;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 18px;
        padding: 14px;
    }

    .stFileUploader>div>div {
        background: #111111;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 18px;
    }

    textarea:disabled {
        color: #f7f7f7;
    }

    @media (max-width: 720px) {
        .section-card {
            padding: 22px;
        }

        .stButton>button,
        .stDownloadButton>button {
            min-height: 50px;
        }
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


initialize_session_state()

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def check_api_keys() -> bool:
    """Check if required API keys are configured."""
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    gemini_key = os.getenv("GEMINI_API_KEY")

    if not openrouter_key and not gemini_key:
        st.error("OPENROUTER_API_KEY or GEMINI_API_KEY is required. Please set one in your .env file.")
        return False

    if not openrouter_key:
        st.warning("OpenRouter key is not configured. Some workflows will use Gemini where available.")

    if not gemini_key:
        st.info("Gemini key is not configured. Summary and review may use OpenRouter fallback.")

    return True


def process_document(file_content, filename: str) -> bool:
    """Process uploaded document and extract text."""
    try:
        temp_file_path = os.path.join("uploads", filename)
        os.makedirs("uploads", exist_ok=True)

        with open(temp_file_path, "wb") as f:
            f.write(file_content)

        is_valid, message = validate_file(temp_file_path)
        if not is_valid:
            st.error(f"File validation failed: {message}")
            return False

        text = extract_text(temp_file_path)
        if not text or not text.strip():
            st.error("Could not extract text from document. Please check the file format.")
            return False

        st.session_state.document_text = text
        st.session_state.filename = filename
        st.session_state.uploaded_file = temp_file_path
        st.session_state.input_text = ""
        st.session_state.results = {
            "document_agent": None,
            "summary_agent": None,
            "info_agent": None
        }

        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

        st.success(f"Document loaded successfully ({len(text)} characters)")
        return True
    except Exception as e:
        st.error(f"Error processing document: {str(e)}")
        return False


def run_document_agent() -> bool:
    """Run the Document Review agent."""
    try:
        with st.spinner("Document Review running..."):
            agent = DocumentAgent()
            result = agent.process_document(st.session_state.document_text)

            if result["status"] == "success":
                st.session_state.results["document_agent"] = result
                st.success("Document Review completed.")
                return True

            st.error(f"Document Review failed: {result.get('message', 'Unknown error')}")
            return False
    except Exception as e:
        st.error(f"Document Review error: {str(e)}")
        return False


def run_summary_agent() -> bool:
    """Run the Summary agent."""
    try:
        with st.spinner("Summary generation running..."):
            agent = SummaryAgent()
            result = agent.process_document(st.session_state.document_text)

            if result["status"] == "success":
                st.session_state.results["summary_agent"] = result
                st.success("Summary generation completed.")
                return True

            st.error(f"Summary generation failed: {result.get('message', 'Unknown error')}")
            return False
    except Exception as e:
        st.error(f"Summary generation error: {str(e)}")
        return False


def run_info_agent() -> bool:
    """Run the Information Extraction agent."""
    try:
        with st.spinner("Information extraction running..."):
            agent = InfoAgent()
            result = agent.process_document(st.session_state.document_text)

            if result["status"] == "success":
                st.session_state.results["info_agent"] = result
                st.success("Information extraction completed.")
                return True

            st.error(f"Information extraction failed: {result.get('message', 'Unknown error')}")
            return False
    except Exception as e:
        st.error(f"Information extraction error: {str(e)}")
        return False


def create_download_data(content: str) -> bytes:
    """Return byte content for Streamlit downloads."""
    return content.encode("utf-8")


def build_combined_report() -> str:
    """Build a unified report containing all available agent results."""
    document_result = st.session_state.results.get("document_agent") or {}
    summary_result = st.session_state.results.get("summary_agent") or {}
    info_result = st.session_state.results.get("info_agent") or {}

    summary_text = summary_result.get("executive_summary") or summary_result.get("bullet_summary") or summary_result.get("key_takeaways") or "Not available."

    return f"""# ========================
DOCUMENT REVIEW
# ========================

IMPROVED DOCUMENT
{document_result.get('improved_document', 'Not available.')}

CHANGES SUMMARY
{document_result.get('changes_summary', 'Not available.')}

# ========================
SUMMARY
# ========================

{summary_text}

# ========================
INFORMATION EXTRACTION
# ========================

IMPORTANT ENTITIES
{info_result.get('entities', 'Not available.')}

DATES AND DEADLINES
{info_result.get('dates_deadlines', 'Not available.')}

ACTION ITEMS
{info_result.get('action_items', 'Not available.')}

DISTRIBUTION REPORT
{info_result.get('distribution_report', 'Not available.')}
"""


# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    st.markdown("""
        <div class='app-shell'>
            <div class='section-card'>
                <div class='section-header'>Agentic AI Document Assistant</div>
                <div class='section-subtitle'>A polished multi-agent document workflow for academic demonstrations.</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    if not check_api_keys():
        st.stop()

    st.markdown("""
        <div class='section-card'>
            <div class='section-header'>Upload Document</div>
            <div class='section-subtitle'>Upload a PDF, DOCX, or TXT file. Or paste text directly if no file is available.</div>
        </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        label="",
        type=["pdf", "docx", "txt"],
        label_visibility="collapsed"
    )

    st.session_state.input_text = st.text_area(
        label="",
        value=st.session_state.input_text,
        height=220,
        placeholder="Paste text here if no file is uploaded..."
    )

    if st.button("Load Content", key="load_content", use_container_width=True):
        if uploaded_file is not None:
            process_document(uploaded_file.getvalue(), uploaded_file.name)
        elif st.session_state.input_text and st.session_state.input_text.strip():
            st.session_state.document_text = st.session_state.input_text.strip()
            st.session_state.filename = "manual_text"
            st.session_state.results = {
                "document_agent": None,
                "summary_agent": None,
                "info_agent": None
            }
            st.success(f"Document loaded successfully ({len(st.session_state.document_text)} characters)")
        else:
            st.error("Please upload a document or paste text to continue.")

    if st.session_state.document_text:
        preview = st.session_state.document_text[:600]
        st.markdown("""
            <div class='section-card'>
                <div class='section-header'>Loaded Content</div>
            </div>
        """, unsafe_allow_html=True)
        st.text_area("Document preview", value=preview, height=180, disabled=True)
        st.markdown(f"<div class='secondary-text'>Source: {st.session_state.filename}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='secondary-text'>Length: {len(st.session_state.document_text)} characters</div>", unsafe_allow_html=True)

        st.markdown("""
            <div class='section-card'>
                <div class='section-header'>Agent Overview</div>
                <div class='section-subtitle'>Run each agent in sequence and download the polished output immediately below the result.</div>
                <div class='secondary-text'>Document Review, Summarization, and Information Extraction remain independent while preserving your existing workflow.</div>
            </div>
        """, unsafe_allow_html=True)

        # Document Review Section
        st.markdown("""
            <div class='section-card'>
                <div class='section-header'>DOCUMENT REVIEW</div>
                <div class='section-subtitle'>Professional document refinement in one clean result card.</div>
            </div>
        """, unsafe_allow_html=True)

        if st.button("Process Document Review", key="document_review", use_container_width=True):
            run_document_agent()

        if st.session_state.results["document_agent"]:
            result = st.session_state.results["document_agent"]
            combined_output = f"""Improved Document:
{result.get('improved_document', '')}

Changes Summary:
{result.get('changes_summary', '')}
"""
            st.markdown("<div class='result-card'>", unsafe_allow_html=True)
            st.markdown("<div class='result-header'>Document Review Result</div>", unsafe_allow_html=True)
            st.text_area("", value=combined_output, height=340, disabled=True)
            st.markdown("</div>", unsafe_allow_html=True)
            st.download_button(
                label="Download Improved Document",
                data=create_download_data(combined_output),
                file_name=f"improved_{st.session_state.filename}.txt",
                mime="text/plain",
                use_container_width=True,
                key="download_improved_document"
            )

        # Summarization Section
        st.markdown("""
            <div class='section-card'>
                <div class='section-header'>SUMMARIZATION</div>
                <div class='section-subtitle'>A concise final summary suitable for presentation and viva review.</div>
            </div>
        """, unsafe_allow_html=True)

        if st.button("Generate Summary", key="generate_summary", use_container_width=True):
            run_summary_agent()

        if st.session_state.results["summary_agent"]:
            result = st.session_state.results["summary_agent"]
            summary_text = result.get("executive_summary") or result.get("bullet_summary") or result.get("key_takeaways") or "No summary available."
            st.markdown("<div class='result-card'>", unsafe_allow_html=True)
            st.markdown("<div class='result-header'>Summary Result</div>", unsafe_allow_html=True)
            st.text_area("", value=summary_text, height=320, disabled=True)
            st.markdown("</div>", unsafe_allow_html=True)
            st.download_button(
                label="Download Summary",
                data=create_download_data(summary_text),
                file_name=f"summary_{st.session_state.filename}.txt",
                mime="text/plain",
                use_container_width=True,
                key="download_summary"
            )

        # Information Extraction Section
        st.markdown("""
            <div class='section-card'>
                <div class='section-header'>INFORMATION EXTRACTION</div>
                <div class='section-subtitle'>Combined entities, dates, actions, and distribution insights in one view.</div>
            </div>
        """, unsafe_allow_html=True)

        if st.button("Extract Information", key="extract_information", use_container_width=True):
            run_info_agent()

        if st.session_state.results["info_agent"]:
            result = st.session_state.results["info_agent"]
            combined_output = f"""Important Entities:
{result.get('entities', '')}

Dates and Deadlines:
{result.get('dates_deadlines', '')}

Action Items:
{result.get('action_items', '')}

Distribution Report:
{result.get('distribution_report', '')}
"""
            st.markdown("<div class='result-card'>", unsafe_allow_html=True)
            st.markdown("<div class='result-header'>Information Extraction Result</div>", unsafe_allow_html=True)
            st.text_area("", value=combined_output, height=380, disabled=True)
            st.markdown("</div>", unsafe_allow_html=True)
            st.download_button(
                label="Download Information Report",
                data=create_download_data(combined_output),
                file_name=f"info_report_{st.session_state.filename}.txt",
                mime="text/plain",
                use_container_width=True,
                key="download_information_report"
            )

        # Export Section
        st.markdown("""
            <div class='section-card'>
                <div class='section-header'>EXPORT</div>
                <div class='section-subtitle'>Download a single combined report for presentations and viva demonstrations.</div>
            </div>
        """, unsafe_allow_html=True)

        st.download_button(
            label="Download Complete Report",
            data=create_download_data(build_combined_report()),
            file_name=f"complete_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True,
            key="download_all_results"
        )


if __name__ == "__main__":
    main()
