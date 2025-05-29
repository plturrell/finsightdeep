#!/bin/bash

# AIQToolkit - NVIDIA Web UI Deployment Script
# This script automates the deployment of the NVIDIA Web UI to Vercel

# Set colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Print banner
echo -e "${GREEN}"
echo "╔══════════════════════════════════════════════════════╗"
echo "║                                                      ║"
echo "║  AIQToolkit - NVIDIA Web UI Deployment to Vercel     ║"
echo "║                                                      ║"
echo "╚══════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check if vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo -e "${YELLOW}Vercel CLI not found. Installing...${NC}"
    npm install -g vercel
fi

# Check if we're in the right directory
if [ ! -f "vercel.json" ] || [ ! -d "api" ]; then
    echo -e "${RED}Error: Please run this script from the web-ui directory containing vercel.json and api folder.${NC}"
    exit 1
fi

# Check for required files
required_files=("package.json" "vercel.json" "index.html" "requirements.txt")
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo -e "${RED}Error: Required file $file not found.${NC}"
        exit 1
    fi
done

echo -e "${GREEN}✓ All required files found.${NC}"

# Ask for NVIDIA API key (with default from vercel.json if present)
current_api_key=$(grep -o '"NVIDIA_API_KEY": "[^"]*"' vercel.json | cut -d'"' -f4)
if [ -z "$current_api_key" ]; then
    current_api_key=""
fi

read -p "Enter your NVIDIA API key [$current_api_key]: " nvidia_api_key
nvidia_api_key=${nvidia_api_key:-$current_api_key}

# Ask for NVIDIA endpoint (with default from vercel.json if present)
current_endpoint=$(grep -o '"NVIDIA_ENDPOINT": "[^"]*"' vercel.json | cut -d'"' -f4)
if [ -z "$current_endpoint" ]; then
    current_endpoint="https://api.nvidia.com/nim/v1"
fi

read -p "Enter your NVIDIA endpoint [$current_endpoint]: " nvidia_endpoint
nvidia_endpoint=${nvidia_endpoint:-$current_endpoint}

# Update vercel.json with the provided API key and endpoint
echo "Updating vercel.json with your API key and endpoint..."
sed -i.bak "s|\"NVIDIA_API_KEY\": \"[^\"]*\"|\"NVIDIA_API_KEY\": \"$nvidia_api_key\"|g" vercel.json
sed -i.bak "s|\"NVIDIA_ENDPOINT\": \"[^\"]*\"|\"NVIDIA_ENDPOINT\": \"$nvidia_endpoint\"|g" vercel.json
rm vercel.json.bak

echo -e "${GREEN}✓ vercel.json updated successfully.${NC}"

# Deployment options
echo -e "\n${YELLOW}Deployment Options:${NC}"
echo "1) Deploy via Vercel CLI (recommended for quick deploy)"
echo "2) Setup GitHub repository and deploy via Vercel GitHub integration"
read -p "Select deployment option [1]: " deploy_option
deploy_option=${deploy_option:-1}

if [ "$deploy_option" = "1" ]; then
    # Deploy via Vercel CLI
    echo -e "\n${YELLOW}Deploying to Vercel...${NC}"
    vercel --prod
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Deployment successful!${NC}"
        echo -e "Your site is now live. You can access it at the URL shown above."
    else
        echo -e "${RED}× Deployment failed. Please check the error message above.${NC}"
    fi
    
elif [ "$deploy_option" = "2" ]; then
    # GitHub deployment
    echo -e "\n${YELLOW}Setting up GitHub repository...${NC}"
    
    # Ask for GitHub username
    read -p "Enter your GitHub username: " github_username
    if [ -z "$github_username" ]; then
        echo -e "${RED}Error: GitHub username is required.${NC}"
        exit 1
    fi
    
    # Ask for repository name
    read -p "Enter repository name [aiqtoolkit-nvidia-ui]: " repo_name
    repo_name=${repo_name:-aiqtoolkit-nvidia-ui}
    
    # Check if git is installed
    if ! command -v git &> /dev/null; then
        echo -e "${RED}Error: git is not installed. Please install git and try again.${NC}"
        exit 1
    fi
    
    # Initialize git if not already initialized
    if [ ! -d ".git" ]; then
        git init
    fi
    
    # Add all files
    git add .
    
    # Commit changes
    git commit -m "Initial commit: AIQToolkit NVIDIA Web UI"
    
    # Create GitHub repository
    echo -e "\n${YELLOW}Creating GitHub repository: $github_username/$repo_name${NC}"
    echo "Please visit: https://github.com/new"
    echo "Create a new repository with name: $repo_name"
    echo "DO NOT initialize with README, .gitignore, or license"
    
    read -p "Press Enter once you've created the repository... "
    
    # Add remote
    git remote add origin "https://github.com/$github_username/$repo_name.git"
    
    # Push to GitHub
    git push -u origin master 2>/dev/null || git push -u origin main
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Successfully pushed to GitHub!${NC}"
        
        # Instructions for Vercel deployment
        echo -e "\n${YELLOW}Now let's deploy to Vercel from GitHub:${NC}"
        echo "1. Go to https://vercel.com/new"
        echo "2. Import your GitHub repository: $repo_name"
        echo "3. Configure your project:"
        echo "   - Framework Preset: Other"
        echo "   - Root Directory: ./"
        echo "   - Build Command: (leave empty)"
        echo "   - Output Directory: ./"
        echo "4. In Environment Variables, add:"
        echo "   - NVIDIA_API_KEY: $nvidia_api_key"
        echo "   - NVIDIA_ENDPOINT: $nvidia_endpoint"
        echo "5. Click 'Deploy'"
        
        read -p "Press Enter once you've completed the deployment... "
        echo -e "${GREEN}Congratulations! Your AIQToolkit NVIDIA Web UI should now be deployed on Vercel.${NC}"
    else
        echo -e "${RED}× Failed to push to GitHub. Please check your repository settings and try again.${NC}"
    fi
    
else
    echo -e "${RED}Invalid option selected.${NC}"
    exit 1
fi

echo -e "\n${GREEN}================ DEPLOYMENT COMPLETE =================${NC}"
echo -e "Don't forget to check the status of your services at: YOUR-URL/public/control-tower.html"
echo -e "To update your deployment in the future, run 'vercel --prod' or push to your GitHub repository."
echo -e "${YELLOW}Thank you for using AIQToolkit!${NC}"