"""
Utils package
Contains utility functions and prompt templates
"""

from .file_handler import (
    extract_text,
    extract_text_from_pdf,
    extract_text_from_docx,
    extract_text_from_txt,
    save_text_to_file,
    validate_file,
    get_file_size_mb
)

from .prompts import (
    get_document_agent_prompt,
    get_summary_agent_prompt,
    get_info_agent_prompt,
    DOCUMENT_AGENT_SYSTEM,
    SUMMARY_AGENT_SYSTEM,
    INFO_AGENT_SYSTEM
)

__all__ = [
    "extract_text",
    "extract_text_from_pdf",
    "extract_text_from_docx",
    "extract_text_from_txt",
    "save_text_to_file",
    "validate_file",
    "get_file_size_mb",
    "get_document_agent_prompt",
    "get_summary_agent_prompt",
    "get_info_agent_prompt"
]
