# Deploying to Vercel

## Prerequisites
1. Create a Vercel account at https://vercel.com if you don't have one
2. Login to Vercel CLI

## Step-by-Step Deployment

1. **Login to Vercel**:
   ```bash
   vercel login
   ```
   This will open your browser for authentication.

2. **Deploy the project**:
   ```bash
   cd /Users/apple/projects/AIQToolkit/web-ui
   vercel --prod
   ```

3. **During deployment, Vercel will ask**:
   - Set up and deploy? (Y)
   - Which scope? (Choose your account)
   - Link to existing project? (N)
   - Project name? (aiqtoolkit-nvidia-ui or your choice)
   - Directory? (./)

4. **Configure environment variables**:
   After deployment, go to your Vercel dashboard:
   - Select your project
   - Go to Settings → Environment Variables
   - Add:
     - `NVIDIA_ENDPOINT`: `https://jupyter0-s1ondnjfx.brevlab.com`
     - Any API keys if needed

## Manual Deployment Alternative

If you prefer to deploy through the Vercel website:

1. Go to https://vercel.com/new
2. Import from Git or upload the `/Users/apple/projects/AIQToolkit/web-ui` folder
3. Configure:
   - Framework Preset: Other
   - Build Command: (leave empty)
   - Output Directory: ./
4. Add environment variables in the UI

## Project Structure

```
web-ui/
├── index.html         # Main UI
├── api/
│   └── index.py      # Serverless API
├── vercel.json       # Vercel configuration
├── package.json      # Project metadata
└── requirements.txt  # Python dependencies
```

## After Deployment

Your app will be available at:
- `https://[your-project-name].vercel.app`

The API endpoints will be:
- `https://[your-project-name].vercel.app/api/health`
- `https://[your-project-name].vercel.app/api/generate`

## Local Testing

Before deploying, you can test locally:
```bash
cd /Users/apple/projects/AIQToolkit/web-ui
python -m http.server 3000
```

Then open http://localhost:3000 in your browser.