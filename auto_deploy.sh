#!/bin/bash

# Automated deployment script for AIQToolkit NVIDIA UI

# Generate unique repository name
TIMESTAMP=$(date +%s)
REPO_NAME="aiqtoolkit-reasoning-engine-${TIMESTAMP}"

echo "🚀 Automated Deployment to Vercel"
echo "================================"
echo "Repository: ${REPO_NAME}"

# Check if git is configured
if ! git config user.name > /dev/null 2>&1; then
    echo "Setting up git config..."
    git config --global user.name "plturrell"
    git config --global user.email "plturrell@example.com"
fi

# Initialize repository
cd /Users/apple/projects/AIQToolkit/web-ui
rm -rf .git  # Clean start
git init
git add .
git commit -m "AIQToolkit NVIDIA UI - Ready for deployment"

# Create GitHub repository using gh CLI (if available)
if command -v gh &> /dev/null; then
    echo "Creating GitHub repository..."
    gh repo create ${REPO_NAME} --public --source=. --remote=origin --push
else
    echo "GitHub CLI not found. Creating repository manually..."
    
    # Create a temporary HTML file for easy GitHub repo creation
    cat > create_repo.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>Create GitHub Repo</title>
    <script>
        function createRepo() {
            // Auto-fill the form
            document.getElementById('repo-name').value = '${REPO_NAME}';
            document.getElementById('repo-desc').value = 'AIQToolkit Reasoning Engine with NVIDIA Integration';
            
            // Open GitHub new repo page
            window.open('https://github.com/new?name=${REPO_NAME}&description=AIQToolkit+Reasoning+Engine+NVIDIA', '_blank');
        }
    </script>
</head>
<body onload="createRepo()">
    <h2>Creating GitHub Repository...</h2>
    <p>A new window will open to create your repository.</p>
    <button onclick="createRepo()">Open GitHub</button>
</body>
</html>
EOF
    
    open create_repo.html
    
    echo ""
    echo "Please create the repository on GitHub, then press Enter..."
    read
    
    # Add remote
    git remote add origin https://github.com/plturrell/${REPO_NAME}.git
    
    echo "Pushing to GitHub..."
    git branch -M main
    git push -u origin main
fi

# Create Vercel deployment link
echo ""
echo "Creating Vercel deployment link..."

# URL encode the git URL
REPO_URL="https://github.com/plturrell/${REPO_NAME}"
ENCODED_URL=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$REPO_URL'))")

# Create deployment URL with pre-filled values
VERCEL_URL="https://vercel.com/new/clone?repository-url=$ENCODED_URL&env=NVIDIA_ENDPOINT&envDescription=NVIDIA%20Brev%20Endpoint&envLink=https://brev.nvidia.com&project-name=${REPO_NAME}&repository-name=${REPO_NAME}"

# Create HTML file to open Vercel
cat > deploy_vercel.html << EOF
<!DOCTYPE html>
<html>
<head>
    <title>Deploy to Vercel</title>
    <style>
        body { font-family: Arial; padding: 40px; text-align: center; }
        .btn { 
            background: #000; 
            color: white; 
            padding: 12px 24px; 
            text-decoration: none; 
            border-radius: 5px; 
            display: inline-block;
            margin: 20px;
        }
        .env-note {
            background: #f0f0f0;
            padding: 20px;
            margin: 20px auto;
            max-width: 600px;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <h1>Deploy AIQToolkit to Vercel</h1>
    
    <div class="env-note">
        <h3>Environment Variable to Add:</h3>
        <code>NVIDIA_ENDPOINT = https://jupyter0-s1ondnjfx.brevlab.com</code>
    </div>
    
    <a href="$VERCEL_URL" class="btn" target="_blank">
        Deploy to Vercel
    </a>
    
    <p>Click the button above to deploy your project to Vercel.</p>
    <p>Make sure to add the environment variable during deployment!</p>
    
    <script>
        // Auto-open Vercel
        window.open('$VERCEL_URL', '_blank');
    </script>
</body>
</html>
EOF

echo ""
echo "Opening Vercel deployment page..."
open deploy_vercel.html

echo ""
echo "✅ Setup Complete!"
echo ""
echo "Next steps:"
echo "1. The GitHub repository page should be open - create the repo"
echo "2. The Vercel deployment page should be open - click 'Deploy'"
echo "3. Add the environment variable: NVIDIA_ENDPOINT = https://jupyter0-s1ondnjfx.brevlab.com"
echo ""
echo "Your app will be live at: https://${REPO_NAME}.vercel.app"