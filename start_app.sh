#!/bin/bash
# resource_id: d9d652e6-b947-452e-9664-3569284a1595
# Lang Trak Startup Script
# Ensures the app runs with the virtual environment activated and TTS working

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Project directory
PROJECT_DIR="/home/dawson/code/lang-trak-in-progress"

echo -e "${BLUE}🚀 Starting Lang Trak App${NC}"
echo "=================================="

# Check if we're in the right directory
cd "$PROJECT_DIR"

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo -e "${RED}❌ Virtual environment not found!${NC}"
    echo "Run: python3 -m venv .venv"
    exit 1
fi

# Activate virtual environment
echo -e "${YELLOW}📦 Activating virtual environment...${NC}"
source .venv/bin/activate

# Check if required packages are installed
echo -e "${YELLOW}🔍 Checking dependencies...${NC}"
if ! python -c "import azure.cognitiveservices.speech" 2>/dev/null; then
    echo -e "${YELLOW}⚠️  Installing Azure Speech SDK...${NC}"
    pip install azure-cognitiveservices-speech
fi

# Test TTS functionality
echo -e "${YELLOW}🎵 Testing TTS...${NC}"
python -c "
import sys
sys.path.append('.')
from src.tts_ipa import ipa_tts
status = ipa_tts.get_status_report()
print(f'TTS Backend: {status[\"primary_backend\"]}')
print(f'Azure Available: {status[\"azure_available\"]}')
if not status['azure_available']:
    print('Note: Using fake TTS. Configure Azure Speech Service for real TTS.')
"

# Set default port if not specified
PORT=${PORT:-5001}

echo -e "${GREEN}✅ Starting Flask app on port ${PORT}...${NC}"
echo -e "${BLUE}📱 Access the app at: http://localhost:${PORT}${NC}"
echo -e "${BLUE}🎤 TTS API endpoint: http://localhost:${PORT}/api/tts/ipa${NC}"
echo ""
echo "Press Ctrl+C to stop the server"
echo "=================================="

# Start the Flask app
export PORT="$PORT"
python app.py