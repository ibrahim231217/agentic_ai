a# Quick Start Guide - 5 Minutes Setup

**Get your Agentic AI Document Assistant running in 5 minutes!**

---

## Step 1: Verify Python Installation (1 minute)

```bash
python --version
# Should show Python 3.8 or higher
```

If Python is not installed:
- Download from [python.org](https://www.python.org/downloads/)
- Install and add to PATH

---

## Step 2: Install Dependencies (1 minute)

```bash
# Navigate to project folder
cd c:\coding_foLdER\agentic_AI

# Install requirements
pip install -r requirements.txt

# Verify installation
pip list | findstr streamlit
# Should show: streamlit==1.28.1
```

---

## Step 3: Get API Keys (2 minutes)

### Get OpenRouter Key (Required)

1. Go to https://openrouter.ai
2. Click "Sign in" → "Sign up with Email"
3. Enter email and create password
4. Check email for verification link
5. Click on your profile icon → "Keys"
6. Click "+ Create Key"
7. **Copy the key** (starts with `sk-or-`)

### Get Gemini Key (Optional but Recommended)

1. Go to https://ai.google.dev/
2. Click "Get API Key"
3. Click "Create API Key in new Google Cloud project"
4. Follow prompts (no credit card needed)
5. **Copy the key** (starts with `AIzaSy`)

---

## Step 4: Configure Environment (1 minute)

```bash
# In VS Code, open Terminal → New Terminal

# Navigate to project
cd c:\coding_foLdER\agentic_AI

# Copy template
cp .env.example .env

# Edit .env file (or create new)
```

**Edit `.env` file:**
```
OPENROUTER_API_KEY=paste_your_openrouter_key_here
GEMINI_API_KEY=paste_your_gemini_key_here
OPENROUTER_USERNAME=your_name
```

**Save the file.** Do NOT share this file!

---

## Step 5: Run the Application (1 minute)

```bash
streamlit run app.py
```

**Wait for:** "Local URL: http://localhost:8501"

**Browser automatically opens** → Ready to use!

---

## 🎉 Done! You're Ready to Use the Application

### First Test

1. **Upload a document:**
   - Create a simple test document (TXT file with a paragraph)
   - Or use any existing PDF/DOCX/TXT

2. **Click agents:**
   - Click "Document Agent"
   - Wait for processing
   - See results

3. **Download output:**
   - Click "Download Improved Document"
   - File is saved to your Downloads folder

---

## ⚡ If Something Doesn't Work

### Issue: "command not found: streamlit"

```bash
# Solution: Install streamlit explicitly
pip install streamlit==1.28.1

# Then run
streamlit run app.py
```

### Issue: API Key Error

1. Copy key again from OpenRouter website
2. Check for extra spaces in `.env`
3. Format should be: `OPENROUTER_API_KEY=sk-or-xxxxx`
4. Restart terminal with Ctrl+C, then run again

### Issue: Port 8501 Already in Use

```bash
# Use different port
streamlit run app.py --server.port 8502
```

### Issue: Import Errors

```bash
# Reinstall all packages
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall

# Then run
streamlit run app.py
```

---

## 📚 Next Steps

- Read [README.md](README.md) for detailed documentation
- Check [API_SETUP.md](API_SETUP.md) for advanced API configuration
- See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for detailed help

---

**All set! Open http://localhost:8501 and start processing documents!** 🚀
