# Amazon A+ Content Generator - Local Setup Guide

## Prerequisites

Install these on your local machine:
- **Node.js** (v18 or higher) - [Download](https://nodejs.org/)
- **Python** (v3.9 or higher) - [Download](https://python.org/)
- **MongoDB** (v5.0 or higher) - [Download](https://www.mongodb.com/try/download/community)
- **Yarn** - Run: `npm install -g yarn`

## Quick Start (Local)

### 1. Download Your Code
From Emergent dashboard, click **"Download Code"** or push to GitHub.

### 2. Install MongoDB Locally
```bash
# macOS (using Homebrew)
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community

# Ubuntu/Debian
sudo apt-get install mongodb
sudo systemctl start mongodb

# Windows
# Download and install from mongodb.com, then start MongoDB service
```

### 3. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate it
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Update .env file for local
cat > .env << 'EOF'
MONGO_URL="mongodb://localhost:27017"
DB_NAME="amazon_aplus_generator"
CORS_ORIGINS="http://localhost:3000"
EMERGENT_LLM_KEY=sk-emergent-8A0Cd959cD2D61aE83
JWT_SECRET=your-secret-key-change-in-production-abc123xyz789
EOF

# Start backend
uvicorn server:app --reload --host 0.0.0.0 --port 8000
```

Backend will run at: **http://localhost:8000**

### 4. Frontend Setup (New Terminal)
```bash
cd frontend

# Install dependencies
yarn install

# Update .env for local
cat > .env << 'EOF'
REACT_APP_BACKEND_URL=http://localhost:8000
EOF

# Start frontend
yarn start
```

Frontend will run at: **http://localhost:3000**

## Testing Locally

1. Open browser to **http://localhost:3000**
2. Sign up with any email/password
3. Create a project and test features:
   - Upload images
   - Remove backgrounds
   - Generate AI backgrounds
   - Create A+ content with AI

## Environment Variables Explained

### Backend (.env)
- `MONGO_URL` - Your local MongoDB connection
- `DB_NAME` - Database name
- `EMERGENT_LLM_KEY` - Your Emergent Universal Key for AI features
- `JWT_SECRET` - Secret for authentication tokens

### Frontend (.env)
- `REACT_APP_BACKEND_URL` - Backend API URL (http://localhost:8000 for local)

## Using Your Own API Keys (Optional)

If you want to use your own OpenAI/Google API keys instead of Emergent credits:

1. Get API keys from:
   - OpenAI: https://platform.openai.com/api-keys
   - Google AI: https://makersuite.google.com/app/apikey

2. Update backend/.env:
```bash
OPENAI_API_KEY=sk-your-openai-key
GOOGLE_API_KEY=your-google-key
```

3. Modify `/backend/server.py` to use these keys instead of EMERGENT_LLM_KEY

## Troubleshooting

**MongoDB connection failed?**
- Check MongoDB is running: `brew services list` (macOS) or `sudo systemctl status mongodb` (Linux)
- Verify connection: `mongosh` or `mongo`

**Backend won't start?**
- Check Python version: `python --version` (need 3.9+)
- Reinstall dependencies: `pip install -r requirements.txt`

**Frontend errors?**
- Clear cache: `rm -rf node_modules yarn.lock && yarn install`
- Check Node version: `node --version` (need 18+)

**CORS errors?**
- Ensure backend CORS_ORIGINS includes `http://localhost:3000`
- Restart backend after .env changes

## Production Deployment

For production deployment to services like:
- **Vercel** (frontend) - Ask me: "Deploy to Vercel"
- **Railway/Render** (backend) - Ask me: "Deploy backend to Railway"
- **MongoDB Atlas** (database) - Free tier available

## Need Help?

Ask me:
- "Add [feature name]"
- "Deploy to [platform]"
- "Fix [issue]"
- "How do I [task]"
