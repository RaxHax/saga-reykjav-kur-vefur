#!/bin/bash

# SAGA Reykjavík - Quick Test Script
# Tests all API endpoints quickly without interactive prompts

set -e

FLASK_URL="http://localhost:5000"
INDEXING_URL="http://localhost:8001"

echo "=========================================="
echo "  SAGA REYKJAVÍK - QUICK API TEST"
echo "=========================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test function
test_endpoint() {
    local name=$1
    local method=$2
    local url=$3
    local data=$4

    echo -n "Testing $name... "

    if [ "$method" = "GET" ]; then
        response=$(curl -s -w "\n%{http_code}" "$url")
    else
        response=$(curl -s -w "\n%{http_code}" -X "$method" -H "Content-Type: application/json" -d "$data" "$url")
    fi

    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')

    if [ "$http_code" = "200" ]; then
        echo -e "${GREEN}✓ OK${NC}"
        return 0
    else
        echo -e "${RED}✗ FAILED (HTTP $http_code)${NC}"
        return 1
    fi
}

# Track results
total=0
passed=0

# 1. Flask Health Check
echo "=== Flask Backend Tests ==="
test_endpoint "Flask Health" "GET" "$FLASK_URL/api/health" && ((passed++))
((total++))

# 2. Flask Stats
test_endpoint "Database Stats" "GET" "$FLASK_URL/api/stats" && ((passed++))
((total++))

# 3. Semantic Search
test_endpoint "Semantic Search" "POST" "$FLASK_URL/api/search" '{"query":"test","limit":5}' && ((passed++))
((total++))

# 4. Icelandic Search
test_endpoint "Icelandic Search" "POST" "$FLASK_URL/api/search/icelandic" '{"query":"mynd","limit":5}' && ((passed++))
((total++))

# 5. Hybrid Search
test_endpoint "Hybrid Search" "POST" "$FLASK_URL/api/search/hybrid" '{"text_query":"test","metadata":{},"weights":{"text":0.7,"metadata":0.3},"limit":5}' && ((passed++))
((total++))

echo ""
echo "=== Indexing Service Tests ==="

# 6. Indexing Service Health
test_endpoint "Indexing Health" "GET" "$INDEXING_URL/health" && ((passed++))
((total++))

# 7. List Jobs
test_endpoint "List Jobs" "GET" "$INDEXING_URL/jobs" && ((passed++))
((total++))

echo ""
echo "=========================================="
echo "  TEST RESULTS"
echo "=========================================="
echo ""
echo "Total Tests: $total"
echo -e "Passed: ${GREEN}$passed${NC}"
echo -e "Failed: ${RED}$((total - passed))${NC}"
echo ""

if [ $passed -eq $total ]; then
    echo -e "${GREEN}All tests passed!${NC}"
    exit 0
else
    echo -e "${YELLOW}Some tests failed. Check service status.${NC}"
    exit 1
fi
