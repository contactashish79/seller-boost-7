# Local Development Setup - Fix for emergentintegrations

## Problem

The `emergentintegrations` library is only available in Emergent's cloud platform. For local development, you need to use the standard OpenAI and Google APIs directly.

## Solution - 3 Options

### Option 1: Use Your Own API Keys (Recommended)

Get your own API keys and use standard libraries.

#### Step 1: Get API Keys

**OpenAI (for text generation):**
1. Go to: https://platform.openai.com/api-keys
2. Sign up / Log in
3. Click "Create new secret key"
4. Copy the key (starts with `sk-proj-...`)
5. Cost: ~$0.01-0.05 per A+ description

**Google AI (for image generation):**
1. Go to: https://makersuite.google.com/app/apikey
2. Sign in with Google account
3. Click "Create API Key"
4. Copy the key
5. Cost: Free tier available, then ~$0.10-0.30 per image

#### Step 2: Install Dependencies

```cmd
cd backend
venv\Scripts\activate
pip install -r requirements_local.txt
```

#### Step 3: Update `.env`

Edit `backend\.env`:

**For MongoDB version:**
```
MONGO_URL=mongodb://localhost:27017
DB_NAME=amazon_aplus_generator
CORS_ORIGINS=http://localhost:3000
JWT_SECRET=your-secret-key-change-in-production

# Replace these with your own keys
OPENAI_API_KEY=sk-proj-your-openai-key-here
GOOGLE_API_KEY=your-google-ai-key-here
```

**For PostgreSQL version:**
```
DATABASE_URL=postgresql://postgres:PASSWORD@localhost:5432/amazon_aplus
BASE_URL=http://localhost:8000
CORS_ORIGINS=http://localhost:3000
JWT_SECRET=your-secret-key-change-in-production

# Replace these with your own keys
OPENAI_API_KEY=sk-proj-your-openai-key-here
GOOGLE_API_KEY=your-google-ai-key-here
```

#### Step 4: Use Updated Server File

I'll create a version that uses standard OpenAI and Google APIs.

---

### Option 2: Mock AI Features (For Testing Only)

If you just want to test the UI without AI features:

Edit `backend\.env`:
```
USE_MOCK_AI=true
OPENAI_API_KEY=mock
GOOGLE_API_KEY=mock
```

AI features will return dummy data.

---

### Option 3: Deploy to Emergent (Uses emergentintegrations)

The app works perfectly on Emergent with the Universal Key. Deploy there if you want to use Emergent's credits.

---

## Which Option Should I Use?

| Option | Best For | Cost | Setup Time |
|--------|----------|------|------------|
| **Option 1** (Own Keys) | Production, full control | Pay per use | 5 min |
| **Option 2** (Mock) | UI testing only | Free | 1 min |
| **Option 3** (Emergent) | Using Emergent credits | Emergent credits | Already done |

---

## Quick Fix for MongoDB Version

If you're using MongoDB version (not PostgreSQL):

1. **Install dependencies:**
```cmd
cd backend
venv\Scripts\activate
pip install -r requirements_local.txt
```

2. **I'll create `server_local.py`** that uses standard APIs

3. **Get your API keys** from links above

4. **Update `.env`** with your keys

5. **Replace server.py:**
```cmd
copy server_local.py server.py
```

6. **Start app:**
```cmd
python -m uvicorn server:app --reload --host 0.0.0.0 --port 8000
```

---

## Quick Fix for PostgreSQL Version

Same steps, but use `server_postgres_local.py` instead.

---

## Cost Comparison

**Using Your Own Keys:**
- Text (GPT-4): ~$0.01-0.05 per description
- Images (Gemini): ~$0.10-0.30 per image
- Total per A+ content: ~$0.50-1.00

**Using Emergent Credits:**
- Deducts from your Emergent account balance
- Same approximate costs
- Billed through Emergent

---

## Next Step

Tell me which option you prefer:

1. **"I want to use my own API keys"** → I'll create the updated server files
2. **"Just mock AI for now"** → I'll create a mock version
3. **"Help me get API keys"** → I'll guide you through the process

Which would you like?
