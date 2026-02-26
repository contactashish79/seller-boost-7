#!/bin/bash

# Local Development Setup Script for Amazon A+ Content Generator

echo "🚀 Setting up Amazon A+ Content Generator locally..."

# Check prerequisites
echo ""
echo "Checking prerequisites..."

if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install from https://nodejs.org/"
    exit 1
fi
echo "✅ Node.js $(node --version)"

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install from https://python.org/"
    exit 1
fi
echo "✅ Python $(python3 --version)"

if ! command -v mongod &> /dev/null; then
    echo "⚠️  MongoDB not found. Please install:"
    echo "   macOS: brew install mongodb-community"
    echo "   Ubuntu: sudo apt-get install mongodb"
    echo "   Windows: Download from mongodb.com"
    exit 1
fi
echo "✅ MongoDB installed"

# Setup backend
echo ""
echo "📦 Setting up Backend..."
cd backend

if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null

pip install -q -r requirements.txt
echo "✅ Backend dependencies installed"

# Update .env for local
cat > .env << 'EOF'
MONGO_URL="mongodb://localhost:27017"
DB_NAME="amazon_aplus_generator"
CORS_ORIGINS="http://localhost:3000"
EMERGENT_LLM_KEY=sk-emergent-8A0Cd959cD2D61aE83
JWT_SECRET=your-secret-key-change-in-production-abc123xyz789
EOF
echo "✅ Backend .env configured for local"

cd ..

# Setup frontend
echo ""
echo "📦 Setting up Frontend..."
cd frontend

if ! command -v yarn &> /dev/null; then
    echo "Installing Yarn..."
    npm install -g yarn
fi

yarn install --silent
echo "✅ Frontend dependencies installed"

# Update .env for local
cat > .env << 'EOF'
REACT_APP_BACKEND_URL=http://localhost:8000
EOF
echo "✅ Frontend .env configured for local"

cd ..

# Create start scripts
echo ""
echo "📝 Creating start scripts..."

# Backend start script
cat > start-backend.sh << 'EOF'
#!/bin/bash
cd backend
source venv/bin/activate 2>/dev/null || source venv/Scripts/activate
echo "🚀 Starting Backend on http://localhost:8000"
uvicorn server:app --reload --host 0.0.0.0 --port 8000
EOF
chmod +x start-backend.sh

# Frontend start script
cat > start-frontend.sh << 'EOF'
#!/bin/bash
cd frontend
echo "🚀 Starting Frontend on http://localhost:3000"
yarn start
EOF
chmod +x start-frontend.sh

# Combined start script
cat > start-all.sh << 'EOF'
#!/bin/bash
echo "🚀 Starting Amazon A+ Content Generator..."
echo ""
echo "Starting MongoDB..."
# Try to start MongoDB (different commands for different OS)
brew services start mongodb-community 2>/dev/null || sudo systemctl start mongodb 2>/dev/null || echo "Please start MongoDB manually"
sleep 2

echo ""
echo "Starting Backend..."
./start-backend.sh &
BACKEND_PID=$!
sleep 3

echo ""
echo "Starting Frontend..."
./start-frontend.sh &
FRONTEND_PID=$!

echo ""
echo "✅ All services started!"
echo ""
echo "🌐 Open your browser to: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for user interrupt
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
EOF
chmod +x start-all.sh

echo "✅ Start scripts created"

# Done
echo ""
echo "✅ Setup complete!"
echo ""
echo "📚 Next Steps:"
echo "   1. Start MongoDB: brew services start mongodb-community (macOS)"
echo "   2. Start Backend: ./start-backend.sh"
echo "   3. Start Frontend: ./start-frontend.sh (in new terminal)"
echo ""
echo "   Or start everything at once: ./start-all.sh"
echo ""
echo "🌐 Then open: http://localhost:3000"
echo ""
echo "📖 See README_LOCAL_SETUP.md for detailed instructions"
