# Pre-Launch Verification Checklist

**Complete this checklist before running the application for the first time.**

---

## ✅ Environment Setup

### Python Installation
- [ ] Python 3.8 or higher installed
  - **Check:** `python --version`
  - **Should show:** `Python 3.8.x`, `3.9.x`, `3.10.x`, `3.11.x`, or `3.12.x`
  
- [ ] pip package manager works
  - **Check:** `pip --version`
  - **Should show:** version number

- [ ] Python in PATH (Windows)
  - **Check:** Can run `python` from any directory
  - **Fix:** Reinstall with "Add Python to PATH" checkbox

### Project Structure
- [ ] Main directory exists: `c:\coding_foLdER\agentic_AI\`

- [ ] All subdirectories created:
  ```
  ✓ agents/
  ✓ utils/
  ✓ uploads/
  ✓ outputs/
  ```

- [ ] All core files present:
  ```
  ✓ app.py
  ✓ requirements.txt
  ✓ .env.example
  ✓ README.md
  ```

- [ ] All agent files present:
  ```
  ✓ agents/__init__.py
  ✓ agents/document_agent.py
  ✓ agents/summary_agent.py
  ✓ agents/info_agent.py
  ```

- [ ] All utility files present:
  ```
  ✓ utils/__init__.py
  ✓ utils/file_handler.py
  ✓ utils/prompts.py
  ```

- [ ] Documentation files present:
  ```
  ✓ QUICKSTART.md
  ✓ API_SETUP.md
  ✓ TROUBLESHOOTING.md
  ✓ USAGE_EXAMPLES.md
  ✓ .gitignore
  ```

---

## ✅ Dependencies Installation

### Install Requirements
- [ ] Running command: `pip install -r requirements.txt`
- [ ] Installation completed without errors
- [ ] All packages installed:
  - [ ] streamlit==1.28.1
  - [ ] python-dotenv==1.0.0
  - [ ] requests==2.31.0
  - [ ] PyPDF2==3.0.1
  - [ ] python-docx==0.8.11
  - [ ] aiohttp==3.9.1

### Verify Installation
- [ ] Run: `pip list | grep streamlit`
- [ ] Should show: `streamlit  1.28.1`

- [ ] Test imports:
  ```bash
  python -c "import streamlit; import requests; import PyPDF2; from docx import Document; print('✅ All imports successful')"
  ```
- [ ] Should show: `✅ All imports successful`

---

## ✅ API Keys Configuration

### OpenRouter Setup (REQUIRED)
- [ ] Registered account at https://openrouter.ai
- [ ] Email verified
- [ ] API key generated and copied
- [ ] Key format: `sk-or-xxxxxxxxxxxxxxxxxxxxxxxx`
- [ ] Key is valid and accessible

### Gemini Setup (OPTIONAL but RECOMMENDED)
- [ ] Registered at https://ai.google.dev/
- [ ] API key generated and copied
- [ ] Key format: `AIzaSyxxxxxxxxxxxxxxxxxxxxxxx`
- [ ] API enabled in Google Cloud

### Environment Variables Setup
- [ ] Created `.env` file in project root
  - **Run:** `cp .env.example .env` (Mac/Linux)
  - **Or:** Copy `.env.example` to `.env` manually (Windows)

- [ ] `.env` file content verified:
  ```
  ✓ OPENROUTER_API_KEY=sk-or-your-actual-key
  ✓ GEMINI_API_KEY=AIzaSy-your-actual-key
  ✓ OPENROUTER_USERNAME=your-name
  ```

- [ ] `.env` has correct format:
  - [ ] No spaces around `=` sign
  - [ ] No quotes around values
  - [ ] One setting per line

- [ ] `.env` is in correct location:
  - **Check:** `ls -la .env` from project root
  - **Should show:** `.env` file listed

### Verify API Keys Work
- [ ] Create and run `verify_keys.py`:

```python
# verify_keys.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

or_key = os.getenv("OPENROUTER_API_KEY")
gemini_key = os.getenv("GEMINI_API_KEY")

print("Checking OpenRouter...")
if or_key:
    headers = {"Authorization": f"Bearer {or_key}"}
    resp = requests.get("https://openrouter.ai/api/v1/models", headers=headers, timeout=5)
    print(f"✅ OpenRouter: {resp.status_code}" if resp.status_code == 200 else f"❌ OpenRouter: {resp.status_code}")
else:
    print("❌ OpenRouter key not found")

print("Checking Gemini...")
if gemini_key:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={gemini_key}"
    resp = requests.post(url, json={"contents": []}, timeout=5)
    print(f"✅ Gemini: {resp.status_code}" if resp.status_code == 200 else f"❌ Gemini: {resp.status_code}")
else:
    print("⚠️  Gemini key not found (optional)")
```

- [ ] Run: `python verify_keys.py`
- [ ] Output shows: `✅ OpenRouter: 200`
- [ ] Output shows: `✅ Gemini: 200` or `⚠️ Gemini: (optional)`

---

## ✅ Code Verification

### Check File Integrity
- [ ] Run: `python -m py_compile app.py agents/*.py utils/*.py`
- [ ] No syntax errors shown

### Test Imports
- [ ] Run: `python -c "from agents import DocumentAgent, SummaryAgent, InfoAgent"`
- [ ] Run: `python -c "from utils import extract_text, get_document_agent_prompt"`
- [ ] No import errors

### Verify Module Structure
- [ ] Check agents package:
  ```bash
  python -c "import agents; print(dir(agents))"
  ```
- [ ] Should show DocumentAgent, SummaryAgent, InfoAgent

- [ ] Check utils package:
  ```bash
  python -c "import utils; print(dir(utils))"
  ```
- [ ] Should show file_handler functions

---

## ✅ Pre-Launch Checks

### System Resources
- [ ] At least 500MB free disk space
- [ ] At least 2GB available RAM
- [ ] Internet connection active and stable
  - **Check:** `ping 8.8.8.8` should respond

### Browser Preparation
- [ ] Modern browser installed (Chrome, Firefox, Edge, Safari)
- [ ] Browser not running old cache
  - **Do:** Clear cache before first run: Ctrl+Shift+Delete

### Directory & Permissions
- [ ] Working directory is correct:
  ```bash
  cd c:\coding_foLdER\agentic_AI
  pwd  # Should show project root
  ```

- [ ] Files are readable:
  ```bash
  ls -la app.py  # Should show file
  ```

---

## ✅ First Run Preparation

### Create Test Document
- [ ] Simple test document prepared:
  - [ ] Text file with sample content (easier for first test)
  - [ ] At least 200-500 words
  - [ ] Plain text without formatting (for first test)

**Sample test content:**
```
Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris 
nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in 
reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
```

- [ ] Saved as `.txt`, `.pdf`, or `.docx` file

### Prepare Monitoring
- [ ] Terminal or command prompt open
- [ ] Ready to see startup messages
- [ ] Know how to stop (Ctrl+C)

---

## ✅ Launch Readiness

### Final Checklist Before Running
- [ ] Current directory is: `c:\coding_foLdER\agentic_AI`
- [ ] `.env` file exists and has API keys
- [ ] Test document prepared
- [ ] Browser is open and ready
- [ ] No antivirus/firewall blocking ports
- [ ] System has good internet connection

### Expected Startup Sequence
When you run `streamlit run app.py`, you should see:

```
1. Collecting usage statistics...
2. You can now view your Streamlit app in your browser.
3. Local URL: http://localhost:8501
4. Network URL: http://192.168.x.x:8501 (optional)
5. ... (Streamlit loads in browser)
```

- [ ] Ready to observe this sequence

---

## ✅ Troubleshooting Pre-Checks

### If Installation Fails
- [ ] Python version is 3.8+ : `python --version`
- [ ] pip is up to date: `pip install --upgrade pip`
- [ ] Not in virtual environment with conflicts
- [ ] Disk space available: `df -h .` (at least 500MB)
- [ ] Internet connection stable

### If API Keys Fail
- [ ] `.env` file exists: `ls .env`
- [ ] Keys copied exactly (no extra spaces/characters)
- [ ] Keys are current (not revoked)
- [ ] Internet connection working: `ping openrouter.ai`
- [ ] No corporate firewall blocking APIs

### If App Won't Start
- [ ] Python not running background process: `pkill python` (Mac/Linux)
- [ ] Port 8501 not in use: `netstat -an | grep 8501` (Windows)
- [ ] Try different port: `streamlit run app.py --server.port 8502`
- [ ] Restart terminal completely
- [ ] Try fresh checkout of files

---

## ✅ Success Indicators

### ✅ Environment Ready When:
- [ ] `python --version` shows 3.8+
- [ ] `pip list | grep streamlit` shows version
- [ ] `cat .env | grep OPENROUTER_API_KEY` shows key (masked)
- [ ] `python verify_keys.py` shows ✅ for OpenRouter

### ✅ App Ready to Launch When:
- [ ] `python -c "from app import *"` runs without error
- [ ] Streamlit installed: `streamlit --version` works
- [ ] Test document prepared
- [ ] API keys verified
- [ ] Browser open on http://localhost:8501

### ✅ First Test Successful When:
- [ ] App loads in browser without blank page
- [ ] "📄 Agentic AI Document Assistant" title appears
- [ ] Upload button visible
- [ ] Can select and upload test document
- [ ] "Document Preview" shows extracted text
- [ ] Can click "Document Agent" button and see processing

---

## 🚀 Ready to Launch?

If you checked everything above:

```bash
cd c:\coding_foLdER\agentic_AI
streamlit run app.py
```

**Expected result:**
- Terminal shows: `Local URL: http://localhost:8501`
- Browser opens automatically to the application
- Ready to upload documents and process!

---

## 🆘 If Something Still Fails

1. **Check QUICKSTART.md** - 5 minute setup guide
2. **Check API_SETUP.md** - API configuration help
3. **Check TROUBLESHOOTING.md** - Detailed error solutions
4. **Verify Keys** - Run `verify_keys.py` script
5. **Full Restart** - Kill terminal, delete `.env`, recreate from scratch

---

## 📝 Verification Log

Print this checklist and mark items as you complete them:

```
Date Started: _______________
Python Version: _______________
Pip Version: _______________

API Keys Verified:
- OpenRouter: ✅ ❌ N/A
- Gemini: ✅ ❌ N/A

First Test Document:
- Type: _______________
- Size: _______________
- Location: _______________

App Launch:
- Time: _______________
- Status: ✅ ❌
- Notes: _______________
```

---

**All checked? Ready to process documents!** 🎉

Start with [QUICKSTART.md](QUICKSTART.md) → [API_SETUP.md](API_SETUP.md) → [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md)
