#!/bin/bash
# Pre-workshop testing script
# Run this the day before to ensure everything works

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo "🧪 NeuroHub Workshop Setup Test"
echo "==============================="
echo ""

# Default values
BACKEND_URL="${OMI_API_BASE_URL:-https://neurohub-workshop.fly.dev}"
API_KEY="${OMI_API_KEY:-neurohub_workshop_2024}"

echo "Testing with:"
echo "  Backend: $BACKEND_URL"
echo "  API Key: ${API_KEY:0:20}..."
echo ""

# Test 1: Backend Health
echo -n "1. Testing backend health... "
if curl -s "$BACKEND_URL/health" > /dev/null 2>&1; then
    echo -e "${GREEN}✅ PASS${NC}"
else
    echo -e "${RED}❌ FAIL${NC}"
    echo "   Backend is not responding. Check deployment."
    exit 1
fi

# Test 2: Python Environment
echo -n "2. Testing Python setup... "
if python --version > /dev/null 2>&1; then
    echo -e "${GREEN}✅ PASS${NC}"
else
    echo -e "${RED}❌ FAIL${NC}"
    echo "   Python not found. Students need Python 3.11+"
fi

# Test 3: UV Installation
echo -n "3. Testing UV package manager... "
if uv --version > /dev/null 2>&1; then
    echo -e "${GREEN}✅ PASS${NC}"
else
    echo -e "${YELLOW}⚠️  WARNING${NC}"
    echo "   UV not found. Students will need to install it."
fi

# Test 4: Demo Script
echo -n "4. Testing demo script... "
if [ -f "demo_simple.py" ]; then
    # Create temp env file
    echo "OMI_API_BASE_URL=$BACKEND_URL" > .env.test
    echo "OMI_API_KEY=$API_KEY" >> .env.test
    
    # Try to run demo
    if OMI_API_BASE_URL="$BACKEND_URL" OMI_API_KEY="$API_KEY" python demo_simple.py > /dev/null 2>&1; then
        echo -e "${GREEN}✅ PASS${NC}"
    else
        echo -e "${YELLOW}⚠️  WARNING${NC}"
        echo "   Demo script failed. Check dependencies."
    fi
    
    rm -f .env.test
else
    echo -e "${RED}❌ FAIL${NC}"
    echo "   demo_simple.py not found!"
fi

# Test 5: Connection Script
echo -n "5. Testing connection script... "
if [ -f "scripts/test_omi_connection.py" ]; then
    if OMI_API_BASE_URL="$BACKEND_URL" OMI_API_KEY="$API_KEY" python scripts/test_omi_connection.py > /dev/null 2>&1; then
        echo -e "${GREEN}✅ PASS${NC}"
    else
        echo -e "${YELLOW}⚠️  WARNING${NC}"
        echo "   Connection test failed."
    fi
else
    echo -e "${RED}❌ FAIL${NC}"
    echo "   test_omi_connection.py not found!"
fi

# Test 6: Load Test
echo -n "6. Running mini load test (8 concurrent)... "
if command -v curl > /dev/null 2>&1; then
    success=0
    for i in {1..8}; do
        curl -s "$BACKEND_URL/health" > /dev/null 2>&1 &
    done
    wait
    echo -e "${GREEN}✅ PASS${NC}"
else
    echo -e "${YELLOW}⚠️  SKIPPED${NC}"
fi

echo ""
echo "==============================="
echo "📊 Test Summary"
echo "==============================="

# Show backend status if fly CLI available
if command -v fly > /dev/null 2>&1; then
    echo ""
    echo "Backend Status:"
    fly status -a neurohub-workshop 2>/dev/null | grep -E "State|Deployed" || echo "Could not get Fly status"
fi

echo ""
echo "📝 Workshop Checklist:"
echo "  □ Backend is deployed and healthy"
echo "  □ Demo scripts work correctly"
echo "  □ Documentation is updated"
echo "  □ Handouts are printed/shared"
echo "  □ Backup plan ready (local Docker)"
echo ""

# Generate student test command
echo "📋 Share this test command with students:"
echo ""
echo -e "${YELLOW}curl $BACKEND_URL/health${NC}"
echo ""

echo "🎯 If all tests passed, you're ready for the workshop!"
echo "   Good luck! 🚀"