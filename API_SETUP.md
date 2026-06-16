# API Setup Guide - Detailed Instructions

This guide provides step-by-step instructions to obtain and configure free API keys.

---

## Table of Contents

1. [OpenRouter Setup](#openrouter-setup) - Document & Information Agents
2. [Gemini Setup](#gemini-setup) - Summarization Agent (Optional)
3. [Verify API Keys](#verify-api-keys)
4. [Troubleshooting](#troubleshooting)

---

## OpenRouter Setup

**Used for:**
- Document Agent (grammar & writing improvement)
- Information Agent (entity extraction)
- Fallback for Summary Agent

### Step-by-Step Setup

#### 1. Create Account

- Visit: https://openrouter.ai
- Click "Sign in" in top right
- Click "Sign up"
- Enter your email address
- Create a secure password
- Click "Sign up"

#### 2. Verify Email

- Check your email inbox
- Click verification link
- Confirm email address

#### 3. Create API Key

- After login, click your **profile icon** (top right)
- Click **"Keys"**
- Click **"+ Create Key"** button
- A new key will appear (starts with `sk-or-`)
- Click **copy icon** to copy to clipboard

#### 4. Add to .env File

```bash
# Open .env file in VS Code
# Add this line:
OPENROUTER_API_KEY=sk-or-xxxxxxxxxxxxxxxxxxxxxxxxx
OPENROUTER_USERNAME=your_name_here
```

### Free Models Available

OpenRouter provides free access to:

| Model | Use Case | Context |
|-------|----------|---------|
| `meta-llama/llama-3.3-8b-instruct:free` | Document & Info tasks | 8K tokens |
| `mistralai/mistral-7b-instruct:free` | General tasks | 32K tokens |
| `meta-llama/llama-2-7b-chat:free` | Alternative | 4K tokens |

**Current app uses:** Llama 3.3 8B

### Check Your API Key Works

```bash
# Create test_openrouter.py
```

```python
import requests

API_KEY = "your_key_here"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "HTTP-Referer": "https://test.local"
}

response = requests.get(
    "https://openrouter.ai/api/v1/models",
    headers=headers
)

print(f"Status: {response.status_code}")
if response.status_code == 200:
    print("✅ OpenRouter key is valid!")
    models = response.json()["data"]
    print(f"Available models: {len(models)}")
else:
    print(f"❌ Error: {response.text}")
```

```bash
python test_openrouter.py
```

---

## Gemini Setup

**Used for:**
- Summarization Agent (primary)
- Better summarization quality than alternatives

### Why Use Gemini?

- Free tier is generous
- Excellent summarization capability
- No credit card required
- Easy setup via Google AI Studio

### Step-by-Step Setup

#### 1. Create Google Account (if needed)

- Go to: https://accounts.google.com
- Create new account or use existing Gmail

#### 2. Access Google AI Studio

- Visit: https://ai.google.dev/
- Click "Get API key"
- Click "Create API key in new Google Cloud project"

#### 3. Generate API Key

- Choose project (default is fine)
- Click "Create API key"
- Key appears in blue box (starts with `AIzaSy`)
- Click copy icon

#### 4. Add to .env File

```bash
# Open .env file in VS Code
# Add this line:
GEMINI_API_KEY=AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Check Your API Key Works

```bash
# Create test_gemini.py
```

```python
import requests

API_KEY = "your_key_here"
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={API_KEY}"

payload = {
    "contents": [
        {
            "parts": [
                {"text": "Say 'Hello'"}
            ]
        }
    ]
}

response = requests.post(url, json=payload)

print(f"Status: {response.status_code}")
if response.status_code == 200:
    print("✅ Gemini key is valid!")
    print(response.json()["candidates"][0]["content"]["parts"][0]["text"])
else:
    print(f"❌ Error: {response.text}")
```

```bash
python test_gemini.py
```

### Free Gemini Tier Limits

- **60 requests per minute** - Usually enough
- **1 million tokens per month** - Very generous
- No credit card required
- Can increase limits by adding credit card (won't charge unless you exceed free tier)

---

## Verify API Keys

### Complete Verification Script

Create `verify_keys.py`:

```python
import os
import requests
from dotenv import load_dotenv

load_dotenv()

print("=" * 50)
print("API KEY VERIFICATION")
print("=" * 50)

# Check OpenRouter
print("\n[1] Checking OpenRouter...")
or_key = os.getenv("OPENROUTER_API_KEY")

if not or_key:
    print("❌ OPENROUTER_API_KEY not found in .env")
else:
    try:
        headers = {"Authorization": f"Bearer {or_key}"}
        response = requests.get(
            "https://openrouter.ai/api/v1/models",
            headers=headers,
            timeout=5
        )
        if response.status_code == 200:
            print("✅ OpenRouter key is VALID")
            data = response.json()
            print(f"   Available models: {len(data.get('data', []))}")
        else:
            print(f"❌ OpenRouter error: {response.status_code}")
            print(f"   {response.text[:100]}")
    except Exception as e:
        print(f"❌ OpenRouter error: {str(e)}")

# Check Gemini
print("\n[2] Checking Gemini...")
gemini_key = os.getenv("GEMINI_API_KEY")

if not gemini_key:
    print("⚠️  GEMINI_API_KEY not found in .env")
    print("   (Optional - will use OpenRouter fallback)")
else:
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={gemini_key}"
        response = requests.post(
            url,
            json={"contents": []},
            timeout=5
        )
        if response.status_code == 200:
            print("✅ Gemini key is VALID")
        else:
            print(f"❌ Gemini error: {response.status_code}")
            print(f"   {response.text[:100]}")
    except Exception as e:
        print(f"❌ Gemini error: {str(e)}")

# Check .env file
print("\n[3] Checking .env file...")
if os.path.exists(".env"):
    print("✅ .env file exists")
else:
    print("❌ .env file not found")
    print("   Create by copying .env.example to .env")

print("\n" + "=" * 50)
print("Verification complete!")
print("=" * 50)
```

Run it:

```bash
python verify_keys.py
```

Expected output:

```
==================================================
API KEY VERIFICATION
==================================================

[1] Checking OpenRouter...
✅ OpenRouter key is VALID
   Available models: 450+

[2] Checking Gemini...
✅ Gemini key is VALID

[3] Checking .env file...
✅ .env file exists

==================================================
Verification complete!
==================================================
```

---

## Troubleshooting

### "Could not find OpenRouter API key"

**Issue:** `.env` file not found or key not set

**Solutions:**

```bash
# 1. Check .env exists
ls -la | grep .env
# Should show: .env.example and .env

# 2. Verify .env format
cat .env
# Should show: OPENROUTER_API_KEY=sk-or-...

# 3. Check for spaces or typos
# Correct: OPENROUTER_API_KEY=sk-or-xxx
# Wrong:   OPENROUTER_API_KEY = sk-or-xxx  (spaces!)
# Wrong:   OPEN_ROUTER_API_KEY=sk-or-xxx   (underscore!)

# 4. Restart app
# Ctrl+C in terminal
# streamlit run app.py
```

### "Invalid API key" Error

**Issue:** Key is wrong or expired

**Solutions:**

```bash
# 1. Verify key format
# OpenRouter: starts with "sk-or-"
# Gemini: starts with "AIzaSy"

# 2. Get fresh key
# Visit https://openrouter.ai/api/keys
# Delete old key
# Create new key
# Update .env

# 3. Test key directly
curl -H "Authorization: Bearer YOUR_KEY" \
     https://openrouter.ai/api/v1/models
```

### "Rate limit exceeded"

**Issue:** Too many API calls

**Solutions:**

```bash
# Wait 60 seconds
# Free tier: 60 requests/min for Gemini
# OpenRouter: depends on model

# For Gemini, add credit card to increase limits:
# 1. Go to https://console.cloud.google.com
# 2. Add payment method (won't charge for free tier)
# 3. Limits increase significantly
```

### "Connection timeout"

**Issue:** Internet connection or API server down

**Solutions:**

```bash
# 1. Check internet
ping google.com

# 2. Wait and retry
# Servers may be temporarily down

# 3. Check service status
# OpenRouter: https://status.openrouter.ai
# Gemini: https://www.google.com/appsstatus
```

### Key works in test but not in app

**Issue:** Different .env files or environment not loaded

**Solutions:**

```bash
# 1. Ensure .env is in project root
cd c:\coding_foLdER\agentic_AI
ls .env  # Should exist

# 2. Restart Streamlit
# Ctrl+C
# streamlit run app.py

# 3. Check Streamlit logs
# Should see: Loaded environment variables from .env
```

---

## API Limits & Quotas

### OpenRouter Free Tier

| Limit | Value |
|-------|-------|
| Rate Limit | No strict limit (fair usage) |
| Models | 100+ free models available |
| Monthly Cost | $0 (free tier) |
| Best For | Development, testing |

### Gemini Free Tier

| Limit | Value |
|-------|-------|
| Requests/min | 60 |
| Tokens/month | 1,000,000 |
| Models | Limited to gemini-pro |
| Monthly Cost | $0 (free tier) |
| Best For | Development, testing |

---

## Best Practices

### Security

```bash
# 1. Never commit .env to git
echo ".env" >> .gitignore

# 2. Use separate keys for development/production
# Dev key: Limited scope
# Prod key: Full permissions (for Phase 2)

# 3. Rotate keys quarterly
# Delete old key, create new one

# 4. Monitor usage
# OpenRouter: https://openrouter.ai/usage
# Gemini: https://console.cloud.google.com
```

### Cost Management

```bash
# 1. Use free tier only during development
# 2. Monitor API usage regularly
# 3. Set up alerts (if available)
# 4. Use caching for repeated queries (Phase 2)
# 5. Batch operations when possible
```

### Performance

```bash
# 1. Use appropriate model size
# - Llama 3.3 8B good for most tasks
# - Switch to 70B if better quality needed

# 2. Adjust temperature for different use cases
# - Lower (0.5): Deterministic answers
# - Higher (0.9): Creative answers

# 3. Set reasonable token limits
# - Document Agent: 2000 max
# - Summary Agent: 2000 max
# - Info Agent: 2500 max
```

---

## Need Help?

If you encounter issues:

1. Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for detailed help
2. Verify keys with `verify_keys.py` script
3. Check API service status pages
4. Review .env file format carefully
5. Ensure internet connection is stable

**All set! Your API keys are ready to use.** 🚀
