# Quick Fix - Run App Locally WITHOUT emergentintegrations

## The Problem
`emergentintegrations` is a private package only available on Emergent platform.

## Fastest Solution (5 minutes)

### Step 1: Update requirements.txt

```cmd
cd backend
```

Edit `requirements.txt` and **REMOVE or comment out** this line:
```
emergentintegrations==0.1.0
```

Or use this command:
```cmd
copy requirements.txt requirements_original.txt
findstr /v "emergentintegrations" requirements_original.txt > requirements.txt
```

### Step 2: Install dependencies
```cmd
venv\Scripts\activate
pip install -r requirements.txt
pip install openai google-generativeai
```

### Step 3: Update server.py

Replace line 19 in `server.py`:

**Remove this:**
```python
from emergentintegrations.llm.chat import LlmChat, UserMessage, ImageContent
```

**Add this:**
```python
import openai
import google.generativeai as genai
```

### Step 4: Update .env

Edit `backend\.env` and add:
```
OPENAI_API_KEY=sk-proj-your-key-here
GOOGLE_API_KEY=your-google-key-here
```

**Don't have keys yet?** Temporarily disable AI features:
```
OPENAI_API_KEY=disabled
GOOGLE_API_KEY=disabled
```

### Step 5: Comment out AI functions temporarily

In `server.py`, find these functions and add `pass` at the start:

```python
@api_router.post("/image/generate-background")
async def generate_background(...):
    raise HTTPException(status_code=501, detail="Configure OPENAI_API_KEY to use this feature")

@api_router.post("/content/generate")
async def generate_content(...):
    raise HTTPException(status_code=501, detail="Configure GOOGLE_API_KEY to use this feature")
```

### Step 6: Run app!

```cmd
:: Backend
cd backend
venv\Scripts\activate
python -m uvicorn server:app --reload --host 0.0.0.0 --port 8000

:: Frontend (new window)
cd frontend
yarn start
```

## What Works

✅ User authentication (signup/login)
✅ Project management (create/view/delete)
✅ Image upload
✅ Image display
✅ Background removal (basic, no AI)
✅ Image enhancement (upscaling)
✅ Full UI/UX

## What Requires API Keys

❌ AI background generation (needs Google AI key)
❌ AI content generation (needs OpenAI key)

## Get API Keys (Optional)

**OpenAI (for text):**
- https://platform.openai.com/api-keys
- $5 minimum, pay per use
- ~$0.01-0.05 per description

**Google AI (for images):**
- https://makersuite.google.com/app/apikey  
- Free tier available
- ~$0.10-0.30 per image

## Or Just Test UI First!

You can test everything except AI features without any API keys. The app will work for:
- Authentication
- Projects
- Image uploads
- Basic image processing

Once you're ready for AI features, get the keys and add them to `.env`

---

**Want me to create a version with proper OpenAI/Google integration?**

Say: "Create server with OpenAI and Google APIs"
