# Agentic AI Document Assistant - Phase 1

##  Project Overview

A beginner-friendly **Agentic AI Document Processing Assistant** built with Streamlit. This Phase 1 prototype demonstrates multiple AI agents working together to process documents using only **free APIs and open-source tools**.

### What It Does

```
User uploads document
    ↓
Text extraction (PDF/DOCX/TXT)
    ↓
┌─────────────────────────────────────────┐
│  Document Agent (Review & Improve)      │
│  Summary Agent (Summarize)              │
│  Information Agent (Extract & Organize) │
└─────────────────────────────────────────┘
    ↓
View results & download reports
```

---

## ✨ Features

### Phase 1 Scope

-  **Document Upload** - PDF, DOCX, TXT files
-  **Text Extraction** - Automatic text processing
-  **Three AI Agents**:
  - **Document Agent**: Grammar correction and writing improvement
  - **Summary Agent**: Executive summaries and key points
  - **Information Agent**: Entity extraction and structured data
-  **Result Display** - Clean UI for viewing AI outputs
-  **Download Functionality** - Export individual or combined reports
-  **Free APIs Only** - No paid subscriptions required
-  **Error Handling** - Graceful error messages and fallbacks
-  **Local Execution** - Run entirely from VS Code

<!-- ### NOT Included (Phase 2+)

-  Authentication / Multi-user support
-  Database storage
-  RAG pipelines or Vector databases
-  Advanced orchestration
-  Deployment/hosting -->

---

##  Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Frontend** | Streamlit | Simple, interactive UI |
| **Backend** | Python | Business logic and API integration |
| **APIs** | OpenRouter, Gemini | Free AI model access |
| **File Processing** | PyPDF2, python-docx | Document parsing |
| **Environment** | python-dotenv | API key management |
| **HTTP** | requests | API communication |

---

##  Architecture Diagram

```
┌─────────────────────────────────────────────────────┐
│           Streamlit Frontend (app.py)               │
│  - File upload UI                                   │
│  - Agent selection buttons                          │
│  - Results display                                  │
│  - Download buttons                                 │
└──────────────────┬──────────────────────────────────┘
                   │
        ┌──────────┼──────────┐
        │          │          │
        ↓          ↓          ↓
    ┌────────┐ ┌────────┐ ┌────────┐
    │Document│ │Summary │ │  Info  │
    │ Agent  │ │ Agent  │ │ Agent  │
    └─┬──────┘ └─┬──────┘ └─┬──────┘
      │          │          │
      ↓          ↓          ↓
  ┌──────────────────────────────────┐
  │  Utility Modules                 │
  │  - File Handler (file_handler.py)│
  │  - Prompts (prompts.py)          │
  │  - Utils (__init__.py)           │
  └──────────────────────────────────┘
      │          │          │
      ↓          ↓          ↓
  ┌─────────┐ ┌─────────┐ ┌──────────┐
  │OpenRouter│ │ Gemini  │ │OpenRouter│
  │(Free)   │ │ (Free)  │ │ (Free)   │
  └─────────┘ └─────────┘ └──────────┘
```

---

## 📦 Project Structure

```
agentic_AI/
│
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── .env.example             # Environment variables template
├── .env                     # Your actual API keys (NOT in git)
│
├── agents/                  # AI Agent modules
│   ├── __init__.py
│   ├── document_agent.py    # Document review and improvement
│   ├── summary_agent.py     # Document summarization
│   └── info_agent.py        # Information extraction
│
├── utils/                   # Utility modules
│   ├── __init__.py
│   ├── file_handler.py      # PDF/DOCX/TXT processing
│   └── prompts.py           # Prompt templates
│
├── uploads/                 # Temporary upload folder (auto-created)
├── outputs/                 # Output folder (auto-created)
│
└── README.md               # This file
```

---

##  Quick Start

### 1. Prerequisites

- Python 3.8 or higher , VS Code (or any terminal) ,  Internet connection (for API calls)

### 2. Setup Instructions

 Step 1: Create Project Structure
Open VS Code and create the following structure (or copy the provided files):

```bash
# Create project directory
mkdir agentic_AI
cd agentic_AI

# Create subdirectories
mkdir agents
mkdir utils
mkdir uploads
mkdir outputs
```

#### Step 2: Install Dependencies

```bash
# Copy all provided files to the project directory

# Install required packages
pip install -r requirements.txt
```

#### Step 3: Get Free API Keys

**Option A: OpenRouter (Recommended - Covers 2 agents)**

1. Go to [https://openrouter.ai](https://openrouter.ai)
2. Sign up for free
3. Click on your profile → "Keys"
4. Generate a new API key
5. Copy the key

**Option B: Gemini (Optional - For better summarization)**

1. Go to [https://ai.google.dev/](https://ai.google.dev/)
2. Click "Get API Key"
3. Create a new project
4. Copy the Gemini API key

#### Step 4: Configure Environment Variables

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your API keys:
   ```
   OPENROUTER_API_KEY=your_openrouter_key_here
   GEMINI_API_KEY=your_gemini_key_here
   OPENROUTER_USERNAME=your_name
   ```

3. **DO NOT** commit `.env` to git (contains secrets!)

### 4. Run the Application

```bash
# From project root directory
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

---

## 📖 How to Use

### Workflow

1. **Upload Document**
   - Click "Choose a document"
   - Select PDF, DOCX, or TXT file
   - View document preview

2. **Select Agents**
   - Click individual agent buttons to process
   - View real-time status updates
   - Each agent works independently

3. **View Results**
   - Expanded sections for each agent
   - See formatted output
   - API used is displayed

4. **Download Results**
   - Individual downloads per agent
   - Combined complete report option
   - All outputs as .txt files

### Example Workflow

**Input:** A project proposal (PDF)

**Processing:**
- Document Agent → Fixes grammar, improves professional tone
- Summary Agent → Extracts executive summary and key points
- Info Agent → Identifies action items, timelines, responsible parties

**Output:** Professional document, summarized version, structured information

---

## 🔑 Free API Keys Guide

### OpenRouter Setup

1. **Create Account:**
   - Visit [openrouter.ai](https://openrouter.ai)
   - Sign up with email
   - Verify email

2. **Generate API Key:**
   - After login, click profile icon → "Keys"
   - Click "Create Key"
   - Copy the generated key

3. **Free Models Available:**
   - `meta-llama/llama-3.3-8b-instruct:free`
   - `mistralai/mistral-7b-instruct:free`
   - Many others at [openrouter.ai/docs/models](https://openrouter.ai/docs/models)

4. **Usage:**
   ```env
   OPENROUTER_API_KEY=sk-or-xxxxxxxxxxxxxxxxxxxxx
   OPENROUTER_USERNAME=your_name
   ```

### Gemini Setup

1. **Create Project:**
   - Visit [ai.google.dev/](https://ai.google.dev/)
   - Click "Get API Key"
   - Create new project or select existing

2. **Generate Key:**
   - Click "Create API Key in Google Cloud Console"
   - Copy the generated key

3. **Usage:**
   ```env
   GEMINI_API_KEY=AIzaSyxxxxxxxxxxxxxxxxxxxxxxx
   ```

### Verify Keys Work

```python
# Quick test script (create as test.py)
import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Test OpenRouter
or_key = os.getenv("OPENROUTER_API_KEY")
if or_key:
    headers = {"Authorization": f"Bearer {or_key}"}
    resp = requests.get("https://openrouter.ai/api/v1/models", headers=headers)
    print(f"OpenRouter: {resp.status_code}")

# Test Gemini
gemini_key = os.getenv("GEMINI_API_KEY")
if gemini_key:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={gemini_key}"
    resp = requests.post(url, json={"contents": []})
    print(f"Gemini: {resp.status_code}")
```

---

## 📝 File-by-File Explanation

### `app.py` (Main Application)
- **Purpose:** Streamlit frontend and orchestration
- **Key Features:**
  - File upload handling
  - Agent execution
  - Results display
  - Download management
  - Error handling
- **Main Functions:**
  - `initialize_session_state()` - Setup Streamlit session
  - `check_api_keys()` - Validate API keys
  - `process_document()` - Extract text from files
  - `run_*_agent()` - Execute individual agents
  - `main()` - Main UI flow

### `agents/document_agent.py`
- **Purpose:** Document review and improvement
- **Capabilities:**
  - Grammar correction
  - Professional rewriting
  - Writing quality improvement
- **Uses:** OpenRouter API
- **Model:** Llama 3.3 8B (free)

### `agents/summary_agent.py`
- **Purpose:** Document summarization
- **Capabilities:**
  - Executive summaries
  - Bullet-point summaries
  - Key takeaways
- **Uses:** Gemini API (primary) or OpenRouter (fallback)

### `agents/info_agent.py`
- **Purpose:** Information extraction and organization
- **Capabilities:**
  - Entity extraction
  - Action item identification
  - Data point extraction
  - Distribution reports
- **Uses:** OpenRouter API
- **Model:** Llama 3.3 8B (free)

### `utils/file_handler.py`
- **Purpose:** Document processing utilities
- **Functions:**
  - `extract_text_from_pdf()` - PDF text extraction
  - `extract_text_from_docx()` - DOCX text extraction
  - `extract_text_from_txt()` - TXT text extraction
  - `extract_text()` - Auto-detect format
  - `validate_file()` - File validation
  - `save_text_to_file()` - Save outputs

### `utils/prompts.py`
- **Purpose:** AI prompt templates
- **Contains:**
  - System prompts for each agent
  - Task prompts with placeholders
  - Prompt formatting functions
  - Response parsing guidelines

### `requirements.txt`
- Lists all Python dependencies
- Install with: `pip install -r requirements.txt`

### `.env.example`
- Template for environment variables
- Copy to `.env` and fill in actual values
- Add `.env` to `.gitignore`

---

## 🐛 Troubleshooting

### Issue: "OPENROUTER_API_KEY not found"

**Solution:**
1. Verify `.env` file exists in project root
2. Check `.env` format: `OPENROUTER_API_KEY=your_key`
3. Restart Streamlit app: `Ctrl+C` then `streamlit run app.py`
4. Verify key from [openrouter.ai](https://openrouter.ai) dashboard

### Issue: "Document extraction failed"

**Solution:**
1. Ensure file is not corrupted
2. Try different format (PDF → DOCX)
3. Check file size (max 50MB)
4. For PDFs, ensure text layer exists (not scan image)
5. Try opening file in native application first

### Issue: "API Error 429 (Rate Limited)"

**Solution:**
1. Wait a few seconds before retrying
2. Check OpenRouter dashboard for usage stats
3. Free tier has rate limits
4. Verify API key is still valid

### Issue: "No module named 'streamlit'"

**Solution:**
```bash
# Reinstall requirements
pip install --upgrade pip
pip install -r requirements.txt

# Or manually install
pip install streamlit==1.28.1
```

### Issue: "Port 8501 already in use"

**Solution:**
```bash
# Use different port
streamlit run app.py --server.port 8502
```

### Issue: Agents produce empty/minimal responses

**Solution:**
1. Try different document
2. Ensure text was extracted (check preview)
3. Verify API keys are correct
4. Check OpenRouter dashboard for issues
5. For Gemini, verify API is enabled in Google Cloud

---

## 🔒 Security Best Practices

1. **Never commit `.env` file**
   ```bash
   echo ".env" >> .gitignore
   ```

2. **Rotate API keys regularly**
   - Delete old keys in OpenRouter/Google Cloud
   - Generate new ones

3. **Use environment variables ONLY**
   - Never hardcode keys in code
   - Never share `.env` files

4. **Limit API permissions**
   - Use OpenRouter keys with minimal scope
   - Restrict Gemini to API key only (no OAuth)

5. **Monitor API usage**
   - Check OpenRouter dashboard for unusual activity
   - Set usage alerts if available

---

## 📊 Performance Considerations

### File Size Limits
- **Maximum:** 50 MB per file
- **Recommended:** < 10 MB for best performance
- **Optimal:** < 5 MB

### Processing Time
- **Document Agent:** 10-30 seconds
- **Summary Agent:** 10-30 seconds
- **Info Agent:** 10-30 seconds
- **Depends on:** File size, API load, internet speed

### Token Limits
- **Document Agent:** ~2000 tokens max
- **Summary Agent:** ~2000 tokens max
- **Info Agent:** ~2500 tokens max
- Longer documents may be truncated

---

## 🚀 Next Steps - Phase 2 Features

Future enhancements not in Phase 1:

- [ ] **User Authentication**
  - Multi-user support
  - User profiles and history

- [ **Database**
  - Store processing history
  - Save user preferences
  - Retrieve past documents

- [ ] **RAG Pipeline**
  - Vector database (Pinecone, Milvus)
  - Semantic search
  - Context-aware responses

- [ ] **Advanced Workflows**
  - Agent chaining
  - Conditional execution
  - Parallel processing

- [ ] **Enhanced UI**
  - Dark mode
  - Custom themes
  - Mobile responsiveness

- [ ] **Deployment**
  - Docker containerization
  - Cloud deployment (AWS, GCP, Azure)
  - CI/CD pipeline

- [ ] **Advanced Agents**
  - Code analysis agent
  - Data analyst agent
  - Translation agent

---

## 📚 Learning Resources

### Python & Streamlit
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Python Requests Library](https://requests.readthedocs.io/)
- [Python python-dotenv](https://github.com/thenv/python-dotenv)

### AI APIs
- [OpenRouter Documentation](https://openrouter.ai/docs)
- [Google Gemini API](https://ai.google.dev/docs)
- [Available Free Models](https://openrouter.ai/docs/models)

### Document Processing
- [PyPDF2 Documentation](https://pypdf2.readthedocs.io/)
- [python-docx Documentation](https://python-docx.readthedocs.io/)

---

## 🤝 Contributing & Feedback

### To Extend This Project

1. **Add New Agent:**
   ```python
   # Create agents/your_agent.py
   class YourAgent:
       def __init__(self, api_key=None):
           # Initialize
       
       def process_document(self, document_text):
           # Your logic
           return results
   ```

2. **Import in app.py**
   ```python
   from agents.your_agent import YourAgent
   ```

3. **Add UI button in app.py**
   ```python
   if st.button("Your Agent"):
       run_your_agent()
   ```

### Common Modifications

- **Change models:** Edit agent files, update model name
- **Modify prompts:** Edit `utils/prompts.py`
- **Add file formats:** Edit `utils/file_handler.py`
- **Change UI:** Edit Streamlit sections in `app.py`

---

## 📜 License

This project is provided as-is for educational purposes.

---

## ❓ FAQ

**Q: Can I use this commercially?**
A: Phase 1 is for learning. For production, consider:
- Authentication and authorization
- Database for data persistence
- Proper error handling and logging
- Rate limiting and cost controls

**Q: What if OpenRouter/Gemini shuts down?**
A: Agents use standard API formats. Easy to switch to:
- Hugging Face Inference API
- Replicate
- Together.ai
- Other free providers

**Q: Can I add my own AI model?**
A: Yes! Edit agent files and use local models with:
- Ollama (local LLMs)
- LM Studio
- vLLM

**Q: How do I deploy this?**
A: Phase 2 consideration. Options:
- Streamlit Cloud (free tier)
- Docker + Kubernetes
- AWS Lambda
- Google Cloud Run

**Q: Can I use this offline?**
A: Currently requires APIs. Future: add Ollama integration for offline mode

**Q: How do I handle large documents?**
A: Current limits: ~50MB file size, ~2500 tokens to API
- Implement document chunking
- Process in sections
- Store intermediate results

---

## 📞 Support

### Having Issues?

1. Check **Troubleshooting** section above
2. Verify API keys in `.env`
3. Check internet connection
4. Review error messages in Streamlit terminal
5. Try with simpler test document

### Common Commands

```bash
# Run application
streamlit run app.py

# Debug mode
streamlit run app.py --logger.level=debug

# Custom port
streamlit run app.py --server.port 8502

# Check dependencies
pip list | grep -E "streamlit|requests|PyPDF2|python-docx"

# Reinstall all
pip install -r requirements.txt --force-reinstall
```

---

**Built with ❤️ using Streamlit, OpenRouter, and Gemini**

**Phase 1 Complete - Ready for Phase 2 Enhancements** ✨
