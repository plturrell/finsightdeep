#!/bin/bash

# AIQToolkit - NVIDIA Web UI Deployment Check Script
# This script checks if the web UI is ready for deployment

# Set colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Checking AIQToolkit Web UI deployment readiness...${NC}"
echo ""

# Check for required files
echo "Checking required files..."
required_files=("package.json" "vercel.json" "index.html" "requirements.txt" "api/index.py" "api/nvidia.py" "api/health.py")
missing_files=()

for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        missing_files+=("$file")
    fi
done

if [ ${#missing_files[@]} -eq 0 ]; then
    echo -e "${GREEN}✓ All required files present${NC}"
else
    echo -e "${RED}✗ Missing required files:${NC}"
    for file in "${missing_files[@]}"; do
        echo "  - $file"
    done
fi

# Check for API keys in source code
echo -e "\nChecking for API keys in source code..."
api_key_files=$(grep -r "nvapi-" --include="*.html" --include="*.py" --include="*.json" --include="*.js" . | grep -v ".example" | grep -v ".gitignore")

if [ -z "$api_key_files" ]; then
    echo -e "${GREEN}✓ No API keys found in source code${NC}"
else
    echo -e "${RED}✗ API keys found in source code:${NC}"
    echo "$api_key_files"
fi

# Check for GitHub repository references
echo -e "\nChecking GitHub repository references..."
github_refs=$(grep -r "github.com/plturrell/finsightdeep" --include="*.html" --include="*.py" --include="*.json" --include="*.md" .)
if [ -n "$github_refs" ]; then
    echo -e "${GREEN}✓ GitHub repository references found${NC}"
else
    echo -e "${YELLOW}! No GitHub repository references found. Make sure repository URLs are updated.${NC}"
fi

# Check for vercel.json configuration
echo -e "\nChecking vercel.json configuration..."
if [ -f "vercel.json" ]; then
    # Check routes
    routes=$(grep -o '"routes":' vercel.json)
    if [ -n "$routes" ]; then
        echo -e "${GREEN}✓ Routes configuration found in vercel.json${NC}"
    else
        echo -e "${RED}✗ No routes configuration found in vercel.json${NC}"
    fi
    
    # Check environment variables
    env_vars=$(grep -o '"env":' vercel.json)
    if [ -n "$env_vars" ]; then
        echo -e "${GREEN}✓ Environment variables section found in vercel.json${NC}"
    else
        echo -e "${RED}✗ No environment variables section found in vercel.json${NC}"
    fi
fi

# Check API CORS configuration
echo -e "\nChecking API CORS configuration..."
cors_missing=()
api_files=$(find api -name "*.py")
for file in $api_files; do
    if ! grep -q "Access-Control-Allow-Origin" "$file"; then
        cors_missing+=("$file")
    fi
done

if [ ${#cors_missing[@]} -eq 0 ]; then
    echo -e "${GREEN}✓ All API files have CORS headers${NC}"
else
    echo -e "${RED}✗ Missing CORS headers in:${NC}"
    for file in "${cors_missing[@]}"; do
        echo "  - $file"
    done
fi

# Check for Python dependencies
echo -e "\nChecking Python dependencies..."
if [ -f "requirements.txt" ]; then
    req_count=$(wc -l < requirements.txt)
    echo -e "${GREEN}✓ requirements.txt found with $req_count dependencies${NC}"
else
    echo -e "${RED}✗ requirements.txt not found${NC}"
fi

# Final summary
echo -e "\n${YELLOW}Deployment Readiness Summary${NC}"
echo "=================================="
echo "1. Remove any API keys from source code before committing"
echo "2. Use environment variables for sensitive information"
echo "3. Follow instructions in DEPLOY_INSTRUCTIONS.md"
echo "4. Test the deployment locally using 'vercel dev' before deploying"
echo "5. After deployment, verify all API endpoints are working"
echo ""
echo -e "${GREEN}Run ./deploy_to_vercel.sh to start the deployment process${NC}"