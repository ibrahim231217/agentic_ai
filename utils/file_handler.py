"""
File handler utilities for document processing.
Supports PDF, DOCX, and TXT file formats.
"""

import os
import PyPDF2
from docx import Document
from pathlib import Path
from typing import Optional


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text from PDF file.
    
    Args:
        file_path: Path to the PDF file
        
    Returns:
        Extracted text from all pages
    """
    try:
        text = []
        with open(file_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            # Extract text from each page
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text.append(page.extract_text())
        
        return '\n'.join(text)
    
    except Exception as e:
        raise ValueError(f"Error extracting text from PDF: {str(e)}")


def extract_text_from_docx(file_path: str) -> str:
    """
    Extract text from DOCX file.
    
    Args:
        file_path: Path to the DOCX file
        
    Returns:
        Extracted text from all paragraphs
    """
    try:
        doc = Document(file_path)
        text = []
        
        # Extract text from each paragraph
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                text.append(paragraph.text)
        
        return '\n'.join(text)
    
    except Exception as e:
        raise ValueError(f"Error extracting text from DOCX: {str(e)}")


def extract_text_from_txt(file_path: str) -> str:
    """
    Extract text from TXT file.
    
    Args:
        file_path: Path to the TXT file
        
    Returns:
        Text content
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as txt_file:
            return txt_file.read()
    
    except UnicodeDecodeError:
        # Try different encoding if UTF-8 fails
        try:
            with open(file_path, 'r', encoding='latin-1') as txt_file:
                return txt_file.read()
        except Exception as e:
            raise ValueError(f"Error extracting text from TXT: {str(e)}")
    
    except Exception as e:
        raise ValueError(f"Error extracting text from TXT: {str(e)}")


def extract_text(file_path: str) -> str:
    """
    Extract text from any supported file format.
    
    Args:
        file_path: Path to the file
        
    Returns:
        Extracted text
    """
    file_extension = Path(file_path).suffix.lower()
    
    if file_extension == '.pdf':
        return extract_text_from_pdf(file_path)
    elif file_extension == '.docx':
        return extract_text_from_docx(file_path)
    elif file_extension == '.txt':
        return extract_text_from_txt(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_extension}")


def save_text_to_file(content: str, filename: str, folder: str = "outputs") -> str:
    """
    Save text content to a file.
    
    Args:
        content: Text content to save
        filename: Name of the output file
        folder: Folder to save the file in
        
    Returns:
        Full path to the saved file
    """
    try:
        # Create folder if it doesn't exist
        os.makedirs(folder, exist_ok=True)
        
        file_path = os.path.join(folder, filename)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return file_path
    
    except Exception as e:
        raise ValueError(f"Error saving file: {str(e)}")


def get_file_size_mb(file_path: str) -> float:
    """
    Get file size in megabytes.
    
    Args:
        file_path: Path to the file
        
    Returns:
        File size in MB
    """
    try:
        file_size_bytes = os.path.getsize(file_path)
        return file_size_bytes / (1024 * 1024)
    except Exception as e:
        raise ValueError(f"Error getting file size: {str(e)}")


def validate_file(file_path: str, max_size_mb: int = 50) -> tuple[bool, str]:
    """
    Validate if file is acceptable.
    
    Args:
        file_path: Path to the file
        max_size_mb: Maximum file size in MB
        
    Returns:
        Tuple of (is_valid, message)
    """
    # Check file extension
    file_extension = Path(file_path).suffix.lower()
    supported_formats = ['.pdf', '.docx', '.txt']
    
    if file_extension not in supported_formats:
        return False, f"Unsupported file format. Supported: {', '.join(supported_formats)}"
    
    # Check file size
    file_size_mb = get_file_size_mb(file_path)
    if file_size_mb > max_size_mb:
        return False, f"File size ({file_size_mb:.2f}MB) exceeds maximum ({max_size_mb}MB)"
    
    # Check if file exists and is readable
    if not os.path.isfile(file_path):
        return False, "File not found"
    
    return True, "File is valid"
