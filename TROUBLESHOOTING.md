# Troubleshooting Guide

Complete troubleshooting guide for common issues with the Agentic AI Document Assistant.

---

## Table of Contents

1. [Installation Issues](#installation-issues)
2. [API Key Issues](#api-key-issues)
3. [File Processing Issues](#file-processing-issues)
4. [Agent Processing Issues](#agent-processing-issues)
5. [Performance Issues](#performance-issues)
6. [General Issues](#general-issues)

---

## Installation Issues

### Issue: "pip: command not found"

**Symptom:** 
```
'pip' is not recognized as an internal or external command
```

**Causes:** Python or pip not installed properly

**Solutions:**

```bash
# 1. Check if Python is installed
python --version

# If not, download from https://www.python.org/downloads/
# IMPORTANT: Check "Add Python to PATH" during installation

# 2. Try python -m pip instead
python -m pip install -r requirements.txt

# 3. If using Python 3.X specifically
python3 -m pip install -r requirements.txt

# 4. Reinstall pip
python -m ensurepip --upgrade

# 5. Verify pip now works
pip --version
```

### Issue: "No module named 'streamlit'"

**Symptom:**
```
ModuleNotFoundError: No module named 'streamlit'
```

**Causes:** Streamlit not installed or installed in wrong environment

**Solutions:**

```bash
# 1. Ensure you're in the project directory
cd c:\coding_foLdER\agentic_AI

# 2. Install streamlit explicitly
pip install streamlit==1.28.1

# 3. If using virtual environment
# Activate it first:
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate
# Then: pip install -r requirements.txt

# 4. Verify installation
python -c "import streamlit; print(streamlit.__version__)"
```

### Issue: "Module not found: PyPDF2, python-docx, requests"

**Symptom:**
```
ModuleNotFoundError: No module named 'PyPDF2'
ModuleNotFoundError: No module named 'docx'
ModuleNotFoundError: No module named 'requests'
```

**Solutions:**

```bash
# 1. Install all requirements at once
pip install -r requirements.txt

# 2. Reinstall with --force-reinstall
pip install -r requirements.txt --force-reinstall

# 3. Install packages individually if needed
pip install PyPDF2==3.0.1
pip install python-docx==0.8.11
pip install requests==2.31.0
pip install streamlit==1.28.1
pip install python-dotenv==1.0.0

# 4. Verify all installed
pip list | grep -E "streamlit|PyPDF2|python-docx|requests|python-dotenv"
```

### Issue: "Permission denied" when installing

**Symptom:**
```
ERROR: Could not install packages due to PermissionError
```

**Solutions:**

```bash
# 1. Install for current user only
pip install --user -r requirements.txt

# 2. Use virtual environment (recommended)
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate

# Then install
pip install -r requirements.txt

# 3. Run as administrator (Windows - last resort)
# Right-click cmd → Run as administrator
# cd c:\coding_foLdER\agentic_AI
# pip install -r requirements.txt
```

---

## API Key Issues

### Issue: "OPENROUTER_API_KEY not found"

**Symptom:**
```
ERROR in app: ValueError: OPENROUTER_API_KEY not found in environment variables
```

**Root Causes:**
- `.env` file doesn't exist
- `.env` not in project root
- API key not set in `.env`
- Wrong variable name

**Solutions:**

```bash
# 1. Verify .env exists
ls -la .env
# If not found:
cp .env.example .env

# 2. Verify .env is in correct location
pwd  # Should show: c:\coding_foLdER\agentic_AI
ls .env  # Should list .env

# 3. Check .env content
cat .env
# Should see: OPENROUTER_API_KEY=sk-or-xxxxx

# 4. Verify key format
# Must be: OPENROUTER_API_KEY=your_actual_key
# Wrong formats:
# OPENROUTER_API_KEY = your_key  (spaces around =)
# OPENROUTER_API_KEY="your_key"  (quotes)
# OPEN_ROUTER_API_KEY=your_key   (underscore instead of dash)

# 5. Restart Streamlit app
# Press Ctrl+C in terminal
# Run again: streamlit run app.py
```

### Issue: "Invalid API key" or "401 Unauthorized"

**Symptom:**
```
OpenRouter API error: 401 - Unauthorized
```

**Causes:**
- API key is wrong or expired
- Copy-paste error
- API key revoked

**Solutions:**

```bash
# 1. Get fresh API key
# Visit https://openrouter.ai
# Login → Profile → Keys
# Delete old key if needed
# Create new key
# Copy exactly (watch for spaces)

# 2. Update .env
OPENROUTER_API_KEY=sk-or-xxxxxxxxxxxxxxxxxxxxxxxx

# 3. Test key outside the app
# Create test_key.py:

import requests

key = "sk-or-your-key-here"
headers = {"Authorization": f"Bearer {key}"}
response = requests.get(
    "https://openrouter.ai/api/v1/models",
    headers=headers
)
print(f"Status: {response.status_code}")

# Run: python test_key.py
# Should show: Status: 200

# 4. Verify no copy errors
# Count characters:
# OpenRouter key should be ~50+ characters

# 5. Restart app
ctrl+c
streamlit run app.py
```

### Issue: "429 Too Many Requests" or Rate Limited

**Symptom:**
```
OpenRouter API error: 429 - Rate limited
Too many requests, please try again later
```

**Causes:**
- Too many API calls in short time
- Hitting rate limits

**Solutions:**

```bash
# 1. Wait 30-60 seconds before retrying

# 2. Reduce frequency of requests
# Don't click buttons rapidly

# 3. Check usage dashboard
# https://openrouter.ai/usage

# 4. For Gemini, rate limits are:
# 60 requests per minute
# 1 million tokens per month

# 5. If developing, space out tests
# Wait 2-3 seconds between API calls

# 6. Upgrade free tier (optional)
# Add payment method to Google Cloud Console
# Increases Gemini limits significantly
```

### Issue: Gemini key works but not used in app

**Symptom:**
App shows "OpenRouter" instead of "Gemini" for summary

**Causes:**
- Gemini key not configured
- Gemini API not enabled
- Streamlit not restarted after adding key

**Solutions:**

```bash
# 1. Verify Gemini key is in .env
# Should have both:
OPENROUTER_API_KEY=sk-or-...
GEMINI_API_KEY=AIzaSy-...

# 2. Restart Streamlit
ctrl+c
streamlit run app.py

# 3. Test Gemini independently
# Create test_gemini.py

import requests
key = "AIzaSy-your-key"
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={key}"
response = requests.post(
    url,
    json={"contents": [{"parts": [{"text": "hi"}]}]}
)
print(f"Status: {response.status_code}")

# Run: python test_gemini.py
# Should show: Status: 200

# 4. Check Gemini API is enabled
# Visit: https://console.cloud.google.com
# Search for "Generative Language API"
# Click Enable if needed
```

---

## File Processing Issues

### Issue: "Unsupported file format"

**Symptom:**
```
ERROR: Unsupported file format
```

**Causes:**
- File extension not supported
- Uploaded file with wrong extension

**Solutions:**

```bash
# 1. Supported formats:
# .pdf - Adobe PDF
# .docx - Microsoft Word
# .txt - Plain text

# 2. Convert file to supported format
# PDF from Word: File → Export as PDF
# Word from PDF: Use online converter or Acrobat
# Text from anything: Open, Copy all, Paste in Notepad

# 3. Check file extension
# File must have correct extension
# Example: document.pdf (not document.PDF or document.text)

# 4. Try different format
# If PDF doesn't work, convert to .txt
# If DOCX doesn't work, try PDF
```

### Issue: "Could not extract text from document"

**Symptom:**
```
ERROR: Could not extract text from document
```

**Causes:**
- PDF is image-based (scanned)
- File is corrupted
- Encoding issues
- File is encrypted

**Solutions:**

```bash
# 1. Check if PDF is scannable image
# Try opening in Adobe Reader
# If you can't copy text, it's image-based
# Solutions:
#   - Use OCR tool (requires additional setup)
#   - Convert via online tool
#   - Ask for original file

# 2. Verify file is not corrupted
# Try opening file in native application
# - PDF: Adobe Reader or browser
# - DOCX: Microsoft Word or Google Docs
# - TXT: Notepad

# 3. Try with different encoding (TXT only)
# File handler tries UTF-8, then Latin-1
# If still fails, file may be damaged

# 4. Check file size
# Maximum: 50 MB
# If larger, may have issues
# Solution: Compress or split file

# 5. Try converting file
# DOCX → PDF: Microsoft Word
# PDF → TXT: Online PDF to text converter
# Corrupt file → Recreate in new document
```

### Issue: "File size exceeds maximum"

**Symptom:**
```
ERROR: File size (75.23MB) exceeds maximum (50MB)
```

**Causes:**
- File is too large

**Solutions:**

```bash
# 1. Check file size
# Right-click file → Properties
# Should be < 50 MB

# 2. Compress file
# PDF: Use online compressor
# DOCX: Save as PDF, then compress
# TXT: Usually small, no compression needed

# 3. Split large file
# Documents: Extract relevant sections
# Reports: Process chapter by chapter
# PDFs: Split into multiple files

# 4. Remove unnecessary content
# Documents: Delete images, formatting
# PDFs: Export text as TXT

# 5. For production (Phase 2)
# Increase limit in code or implement chunking
```

### Issue: "File not found" or "Permission denied"

**Symptom:**
```
ERROR: File not found or permission issues
```

**Causes:**
- File deleted after upload
- No read permissions
- Temporary file issues

**Solutions:**

```bash
# 1. Check file still exists
# Don't delete after upload (processing happens quickly)

# 2. Check permissions
# Right-click file → Properties → Security
# Ensure you have Read permissions
# If not, change permissions or use different file

# 3. Try uploading again
# Sometimes temporary files have issues
# Upload same file again

# 4. Check disk space
# If disk full, file operations fail
# Free up space and retry

# 5. Try different file
# If specific file fails, might be corrupted
# Try with different document
```

---

## Agent Processing Issues

### Issue: "Agent timeout" or "Agent takes too long"

**Symptom:**
App shows loading for 5+ minutes or times out

**Causes:**
- Large document
- Slow internet connection
- API server slow
- Network issues

**Solutions:**

```bash
# 1. Use smaller document
# Start with < 5MB files
# Test with simple text first

# 2. Check internet connection
# ping google.com
# Should show response time < 100ms
# If higher, WiFi may be weak

# 3. Retry later
# API servers may be busy
# Try again in a few minutes

# 4. Try different agent first
# Maybe just one agent is slow
# Helps identify which one

# 5. Check for network issues
# Try on different WiFi or wired connection
# Test if OpenRouter is accessible:
#   curl https://openrouter.ai

# 6. For Phase 2 optimization
# Implement async processing
# Add progress bars and cancellation
```

### Issue: "Empty or minimal agent response"

**Symptom:**
Agent returns almost empty response or generic text

**Causes:**
- Document text too short
- API response empty
- Parsing failed
- API key quota exceeded

**Solutions:**

```bash
# 1. Try with longer document
# Agents need enough content
# Minimum: ~200 words recommended
# Test with 500+ word document

# 2. Verify document content
# Click "Document Preview" button
# Should see actual text
# If preview is empty, extract text failed

# 3. Check if API is responding
# Run verify_keys.py script:
# python verify_keys.py
# Should show "✅ VALID" for both APIs

# 4. Check API quota
# OpenRouter: https://openrouter.ai/usage
# Gemini: Check Google Cloud Console
# May have hit limits

# 5. Try different agent
# If one returns empty, try another
# Helps isolate the issue

# 6. Increase token limits
# Edit agent files, increase max_tokens:
# Change: "max_tokens": 2000
# To:     "max_tokens": 4000
# (Not recommended, uses more credits)

# 7. Review agent prompts
# Edit utils/prompts.py
# Make prompts more specific
# Add examples

# 8. Use different document
# Try simple, well-formatted document
# Original document may confuse AI
```

### Issue: "Agent returns error despite valid key"

**Symptom:**
```
ERROR: Agent error: Invalid request
API error 400 - Bad request
```

**Causes:**
- Malformed API request
- Invalid parameters
- API changed format
- Header issues

**Solutions:**

```bash
# 1. Check agent code matches API spec
# Visit: https://openrouter.ai/docs/api/v1
# Verify format in agent files

# 2. Check payload format
# All JSON must be valid:
# - Strings in quotes: "hello"
# - Numbers without quotes: 123
# - Booleans lowercase: true, false
# - No trailing commas

# 3. Verify headers
# Should include:
# "Authorization": "Bearer KEY"
# "Content-Type": "application/json"

# 4. Check message format
# Messages should be:
# {"role": "user", "content": "text"}
# Not just plain strings

# 5. Try with curl to debug
# curl -X POST https://openrouter.ai/api/v1/chat/completions \
#   -H "Authorization: Bearer YOUR_KEY" \
#   -H "Content-Type: application/json" \
#   -d '{"model":"meta-llama/llama-3.3-8b-instruct:free","messages":[{"role":"user","content":"hi"}],"max_tokens":100}'

# 6. Check API documentation
# Updates happen, API format may change
# https://openrouter.ai/docs

# 7. Report issue if persists
# May be API-side problem
```

---

## Performance Issues

### Issue: "Application is very slow"

**Symptom:**
Buttons take long to respond, UI is sluggish

**Causes:**
- Large document processing
- Network latency
- Limited system resources
- Inefficient code

**Solutions:**

```bash
# 1. Close unnecessary applications
# Free up RAM
# Browsers, other apps use memory

# 2. Check system resources
# Windows: Ctrl+Shift+Esc (Task Manager)
# Mac: Command+Space → Activity Monitor
# Linux: htop
# Look for high CPU/Memory usage

# 3. Use smaller documents for testing
# Start with < 1MB files
# Larger files take longer

# 4. Check internet speed
# Visit: https://www.speedtest.net
# Should be > 10 Mbps for good experience
# If slow, may need different WiFi

# 5. Disable browser extensions
# Some extensions slow down pages
# Try incognito/private mode

# 6. Increase Streamlit resources
# Edit app.py
# Add: st.set_page_config(..., layout="wide")
# Already done in current version

# 7. Run on local machine vs remote
# Remote connections slower
# Process files locally when possible
```

### Issue: "Memory usage keeps increasing"

**Symptom:**
App gets slower over time as you process more documents

**Causes:**
- Session state accumulation
- Temporary files not cleaned
- Memory leaks in libraries

**Solutions:**

```bash
# 1. Restart Streamlit app
# Ctrl+C in terminal
# streamlit run app.py
# Clears all memory

# 2. Clear session state manually
# Each document upload clears it
# Or use browser back button

# 3. Clean temporary files
# Check uploads/ and outputs/ folders
# Delete old files manually

# 4. For Phase 2
# Implement automatic cleanup
# Delete temporary files after processing
# Limit session memory

# 5. Monitor with task manager
# Windows: Ctrl+Shift+Esc
# Python process should use < 500MB
# If > 1GB, definitely a memory leak
```

---

## General Issues

### Issue: "App doesn't start" or "Blank page"

**Symptom:**
```
No errors, but app shows blank page or doesn't load
```

**Causes:**
- Port conflict
- Streamlit issue
- Browser cache
- Import error

**Solutions:**

```bash
# 1. Check if app started
# Terminal should show:
# "Collecting usage statistics..."
# "Local URL: http://localhost:8501"

# If not shown, check for errors above

# 2. Reload browser
# Press F5 or Ctrl+R
# Clear cache: Ctrl+Shift+Delete

# 3. Try different port
streamlit run app.py --server.port 8502

# 4. Check for import errors
# Run: python -c "import app"
# Should succeed with no errors

# 5. Check all files exist
ls -la agents/
ls -la utils/
# All Python files should be present

# 6. Verify .env exists
ls -la .env
# Should show .env file

# 7. Full restart
# Close terminal (Ctrl+C)
# Close browser tab
# Run: streamlit run app.py
# Wait 10 seconds for full startup
```

### Issue: "Downloaded file is empty"

**Symptom:**
Downloaded file has 0 bytes or contains nothing

**Causes:**
- Download interrupted
# No results to download
# File I/O error

**Solutions:**

```bash
# 1. Run agents first
# Make sure you clicked at least one agent button
# Wait for "✅ completed" message

# 2. Try download again
# Click download button again
# Try different browser (Chrome, Firefox, Edge)

# 3. Check browser settings
# Some browsers block auto-download
# Allow downloads from this site
# Check Downloads folder

# 4. Try with different file format
# Each agent has separate download
# All data also in "Complete Report"

# 5. For developers
# Check Streamlit logs for errors
# Look in terminal for:
# "Error generating report"
# "File I/O error"
```

### Issue: "Agents don't work after adding .env"

**Symptom:**
API keys look correct, but agents still fail

**Causes:**
- .env not reloaded
# Keys in wrong format
# Environment not updated

**Solutions:**

```bash
# 1. Restart Streamlit completely
# Ctrl+C in terminal (stop app)
# Wait 2 seconds
# Run: streamlit run app.py

# 2. Verify .env format is perfect
# No spaces: OPENROUTER_API_KEY=sk-or-xxx
# Not:       OPENROUTER_API_KEY = sk-or-xxx
# Not:       OPENROUTER_API_KEY="sk-or-xxx"

# 3. Close all browser tabs
# Close localhost:8501 tab completely
# Reopen: http://localhost:8501

# 4. Check key wasn't copied with extra characters
# Copy from OpenRouter, paste in editor
# Remove any extra spaces/quotes
# Key should start exactly with sk-or- or AIzaSy

# 5. Try using full path in terminal
# From C:\coding_foLdER\agentic_AI
# streamlit run app.py

# 6. Create new .env from scratch
# Delete .env
# cp .env.example .env
# Add keys manually
```

### Issue: "Can't find agents folder"

**Symptom:**
```
ModuleNotFoundError: No module named 'agents'
No module named 'utils'
```

**Causes:**
- Files in wrong location
- Missing __init__.py files
- Wrong working directory

**Solutions:**

```bash
# 1. Verify project structure
# cd c:\coding_foLdER\agentic_AI
# pwd  # Should show full path

# 2. List files/folders
ls -la
# Should show:
# agents/
# utils/
# uploads/
# outputs/
# app.py
# requirements.txt
# .env

# 3. Check __init__.py exists
ls -la agents/__init__.py
ls -la utils/__init__.py
# Both should exist

# 4. Run from correct directory
# You must be in: c:\coding_foLdER\agentic_AI
# NOT in subdirectories

# 5. Check imports in app.py
# Should be:
# from agents.document_agent import DocumentAgent
# from utils.file_handler import extract_text
# (NOT from ..agents import ...)

# 6. Test imports manually
python -c "from agents.document_agent import DocumentAgent"
# Should work with no errors
```

---

## Getting More Help

### Debug Mode

Enable detailed logging:

```bash
streamlit run app.py --logger.level=debug
```

### Check Logs

Look for error messages in terminal where Streamlit runs

### Common Log Messages

| Message | Meaning | Fix |
|---------|---------|-----|
| `Loaded environment variables` | .env found ✅ | Normal |
| `Could not find .env` | .env missing ❌ | Create .env |
| `401 Unauthorized` | Bad API key ❌ | Verify key |
| `Connection timeout` | Network issue ❌ | Check internet |
| `Invalid response format` | API changed ❌ | Update agent code |

### Contact Support

If issue persists:

1. Save error message and logs
2. Note exact steps to reproduce
3. Include Python version: `python --version`
4. Include Streamlit version: `python -c "import streamlit; print(streamlit.__version__)"`
5. Check GitHub issues for similar problems
6. Consider Phase 2 improvements for robustness

---

**Most issues resolve with: full restart (Ctrl+C + streamlit run app.py) and verifying .env keys.** 🔑
