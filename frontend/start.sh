#!/bin/bash
# Start both the API backend and React frontend dev server
# Usage: ./start.sh

DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"

echo "=== TENDERS Dashboard ==="
echo ""

# Install Python deps if needed
if ! python3 -c "import fastapi" 2>/dev/null; then
    echo "Installing Python dependencies..."
    pip3 install -r api/requirements.txt
fi

# Install Node deps if needed
if [ ! -d "node_modules" ]; then
    echo "Installing Node dependencies..."
    npm install
fi

# Start API (background)
echo "Starting API server on http://localhost:8010..."
python3 -c "
import uvicorn, sys
sys.path.insert(0, '.')
from api.main import app
uvicorn.run(app, host='0.0.0.0', port=8010)
" &
API_PID=$!

# Wait for API
sleep 2

# Start frontend dev server
echo "Starting frontend on http://localhost:3000..."
npm run dev &
VITE_PID=$!

echo ""
echo "Dashboard: http://localhost:3000"
echo "API:       http://localhost:8010/api/stats"
echo ""
echo "Press Ctrl+C to stop both servers"

trap "kill $API_PID $VITE_PID 2>/dev/null; exit" INT TERM
wait
