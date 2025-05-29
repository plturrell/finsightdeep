# Deploying AIQToolkit NVIDIA UI to Vercel

This document provides step-by-step instructions for deploying the AIQToolkit NVIDIA UI to Vercel, making it accessible as a web application.

## Prerequisites

1. Create a Vercel account at https://vercel.com
2. Node.js version 18 or higher installed (required for Vercel CLI)
3. Python 3.8 or higher installed (required for API functions)
4. Install the Vercel CLI (required for command-line deployment):
   ```bash
   npm install -g vercel
   ```
5. A GitHub account (recommended for continuous deployment)
6. An NVIDIA API key (obtain from [NVIDIA API Platform](https://developer.nvidia.com/))

## NVIDIA API Key Setup

Before deployment, you'll need a valid NVIDIA API key for authenticating with NVIDIA services:

1. Register or log in at [NVIDIA Developer Portal](https://developer.nvidia.com/)
2. Navigate to the API access section and generate an API key
3. The key should begin with `nvapi-` followed by a unique identifier
4. Keep this key secure and do not share it publicly

## Automatic Deployment Script

For convenience, we provide a deployment script that handles GitHub setup and Vercel deployment:

```bash
# From the project root
chmod +x ./deploy_to_vercel.sh
./deploy_to_vercel.sh
```

This script will guide you through:
- Setting up your NVIDIA API key and endpoint
- Creating a GitHub repository (optional)
- Pushing code to GitHub (optional)
- Connecting the repository to Vercel
- Setting up environment variables

## Manual Deployment Options

### Option 1: Deploy from GitHub (Recommended)

1. **Create a GitHub repository**:
   - Go to https://github.com/new
   - Create a new repository named `finsightdeep`
   - Initialize with a README (optional)

2. **Push the code to GitHub**:
   ```bash
   cd /path/to/AIQToolkit/web-ui
   git init
   git add .
   git commit -m "Initial commit: AIQToolkit NVIDIA UI"
   git remote add origin https://github.com/YOUR_USERNAME/finsightdeep.git
   git push -u origin main
   ```

3. **Deploy to Vercel**:
   - Go to https://vercel.com/new
   - Click "Import Git Repository"
   - Select the repository you just created
   - Configure project:
     - Framework Preset: Other
     - Root Directory: ./
     - Build Command: (leave empty)
     - Output Directory: ./
   - Add Environment Variables:
     - `NVIDIA_ENDPOINT`: `https://api.nvidia.com/nim/v1`
     - `NVIDIA_API_KEY`: Your NVIDIA API key (starts with nvapi-)
   - Click "Deploy"

### Option 2: Deploy via Vercel CLI

1. **Login to Vercel**:
   ```bash
   vercel login
   ```

2. **Deploy the project**:
   ```bash
   cd /path/to/AIQToolkit/web-ui
   vercel --prod
   ```

3. **During deployment, Vercel will ask**:
   - Set up and deploy? (Y)
   - Which scope? (Choose your account)
   - Link to existing project? (N)
   - Project name? (finsightdeep or your choice)
   - Directory? (./)

4. **Configure environment variables**:
   After deployment, go to your Vercel dashboard:
   - Select your project
   - Go to Settings → Environment Variables
   - Add the following environment variables:
     - `NVIDIA_ENDPOINT`: `https://api.nvidia.com/nim/v1`
     - `NVIDIA_API_KEY`: Your NVIDIA API key (starts with nvapi-)

## Project Structure

```
web-ui/
├── index.html            # Main dashboard UI
├── public/               # Static assets and additional pages
│   ├── control-tower.html   # Control tower interface
│   ├── reasoning.html       # Reasoning interface
│   ├── status.html          # System status page
│   └── premium-design-system.css  # Design system
├── api/                  # Serverless API functions
│   ├── index.py          # Main API endpoint
│   ├── health.py         # Health check endpoint
│   ├── generate.py       # Content generation endpoint
│   ├── nvidia.py         # NVIDIA model integration
│   └── reasoning.py      # Reasoning engine endpoint
├── vercel.json           # Vercel configuration
├── package.json          # Project metadata
└── requirements.txt      # Python dependencies
```

## Post-Deployment

After successful deployment, your application will be available at:
- `https://[your-project-name].vercel.app`

The following API endpoints will be accessible:
- `https://[your-project-name].vercel.app/api` - API information
- `https://[your-project-name].vercel.app/api/health` - System health
- `https://[your-project-name].vercel.app/api/generate` - Content generation
- `https://[your-project-name].vercel.app/api/nvidia` - NVIDIA integration
- `https://[your-project-name].vercel.app/api/reasoning` - Reasoning engine

## Local Development & Testing

### Using Vercel CLI for local development (recommended):

```bash
cd /path/to/AIQToolkit/web-ui
# Set up environment variables locally
export NVIDIA_API_KEY="your-nvidia-api-key"
export NVIDIA_ENDPOINT="https://api.nvidia.com/nim/v1"
# Start the development server
vercel dev
```

### Using Python's built-in server (frontend only):

```bash
cd /path/to/AIQToolkit/web-ui
python -m http.server 3000
```

Then open http://localhost:3000 in your browser.

Note: When using Python's server, API functionality will not be available locally. Use this only for frontend development.

## Testing After Deployment

After successful deployment, verify your application is working properly:

1. Visit your application's main URL (`https://[your-project-name].vercel.app`)
2. Check that the dashboard loads correctly and navigation works
3. Visit the Control Tower page (`/public/control-tower.html`) to verify API connections
4. Use the Test Connection buttons to validate NVIDIA service connectivity
5. Verify that the API endpoints return proper responses:
   - `/api/health` - Should return system health status
   - `/api/nvidia` - Test with a sample prompt to verify NVIDIA model access

## Updates and Maintenance

To update your deployed application:

### Via Vercel CLI:
```bash
cd /path/to/AIQToolkit/web-ui
# Make your changes
# Test locally
vercel dev
# Deploy updates
vercel --prod
```

### Via GitHub (if using continuous deployment):
```bash
cd /path/to/AIQToolkit/web-ui
# Make your changes
git add .
git commit -m "Description of changes"
git push origin main
```
Vercel will automatically deploy updates when you push to your GitHub repository.

## Troubleshooting

- **API endpoints return 404**: 
  - Ensure your `vercel.json` file is correctly configured
  - Check that the route configuration matches your API structure
  - Verify that the `/api` directory exists in your deployment

- **CORS errors**: 
  - Verify that the Access-Control-Allow headers are properly set in all API files
  - Check browser console for specific CORS error messages
  - Ensure your frontend is making requests to the correct domain

- **Authentication failures with NVIDIA services**:
  - Verify your NVIDIA API key is valid and not expired
  - Check that the key is correctly set in Vercel environment variables
  - Confirm the key has access to the specific NVIDIA services you're using

- **Environment variables not working**: 
  - Check Vercel dashboard settings and verify they're correctly set
  - Remember that environment variables are only available in production after deploying
  - For local development, set them manually or use a .env file with vercel dev

- **Deployment fails**: 
  - Examine the build logs in Vercel for specific error messages
  - Check that all required files are included in your repository
  - Verify that dependencies are correctly specified in requirements.txt and package.json

## Support and Resources

- NVIDIA API Documentation: [NVIDIA Developer Portal](https://developer.nvidia.com/docs)
- Vercel Deployment Documentation: [Vercel Docs](https://vercel.com/docs)
- AIQToolkit Documentation: [AIQToolkit Docs](https://aiqtoolkit.ai/docs)

For additional support, please contact support@aiqtoolkit.ai