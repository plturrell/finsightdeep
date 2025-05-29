# AIQToolkit NVIDIA UI 🚀

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fplturrell%2Faiqtoolkit-nvidia-ui&env=NVIDIA_ENDPOINT&envDescription=NVIDIA%20Brev%20Endpoint%20URL&envLink=https://brev.nvidia.com&project-name=aiqtoolkit-nvidia-ui)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)
[![NVIDIA Blueprint](https://img.shields.io/badge/NVIDIA-Blueprint-76B900)](https://developer.nvidia.com/)

A modern, responsive web interface for interacting with NVIDIA AI models and services through AIQToolkit. Now with enhanced Vercel deployment support.

## ✨ Features

- **🎯 NVIDIA Integration** - Seamless connection to NVIDIA AI models and services
- **📊 Interactive UI** - Clean, responsive web interface for AI model interaction
- **🖥️ Control Tower** - Real-time monitoring of NVIDIA services and their performance
- **⚡ Serverless Architecture** - Built for Vercel with auto-scaling capabilities
- **🔒 Secure API Proxy** - CORS-enabled API endpoints with environment-based configuration
- **📱 Mobile Responsive** - Works perfectly on desktop, tablet, and mobile devices
- **🚀 One-Click Deploy** - Deploy to Vercel with a single click
- **🔧 Easy Configuration** - Simple environment variable setup
- **💻 Reasoning Interface** - Advanced reasoning with step-by-step explanations
- **🤖 Digital Human Interface** - NVIDIA-powered digital human interactions

## 🚀 Quick Start

### Deploy to Vercel (Recommended)

1. Click the "Deploy with Vercel" button above
2. Add your `NVIDIA_ENDPOINT` environment variable
3. Deploy and start using immediately!

### Alternative Deployment Methods

For detailed deployment instructions, see [DEPLOY_INSTRUCTIONS.md](DEPLOY_INSTRUCTIONS.md).

### Run Locally

```bash
# Clone the repository
git clone https://github.com/plturrell/aiqtoolkit-nvidia-ui.git
cd aiqtoolkit-nvidia-ui

# Option 1: Using Python's built-in server (UI only)
python -m http.server 3000

# Option 2: Using Vercel CLI (full functionality)
npm install -g vercel
vercel dev
```

Visit `http://localhost:3000` to see the main dashboard.

## 📡 NVIDIA Services & Interfaces

The AIQToolkit NVIDIA UI provides access to:

- **Main Dashboard** - Central hub for all NVIDIA services
- **Report Generator** - Create reports using NVIDIA AI models
- **Control Tower** - Monitor NVIDIA services in real-time
- **Reasoning Interface** - Advanced reasoning with step-by-step analysis
- **Digital Human** - Conversational AI with NVIDIA models
- **Blueprint Console** - Command-line interface to NVIDIA services
- **System Status** - Health monitoring of all components

## 📁 Project Structure

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

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `NVIDIA_ENDPOINT` | NVIDIA API endpoint URL | ✅ | None |
| `NVIDIA_API_KEY` | NVIDIA API key for authentication | ❌ | None |

### Vercel Configuration

The `vercel.json` file configures:
- Serverless function routing
- Environment variables
- Build settings
- CORS headers

## 🔌 API Endpoints

- `/api` - API information
- `/api/health` - System health check
- `/api/generate` - Content generation
- `/api/nvidia` - NVIDIA model integration
- `/api/reasoning` - Reasoning engine

### Example: Generate with NVIDIA
```http
POST /api/generate
Content-Type: application/json

{
  "prompt": "Your AI prompt here",
  "model": "nvidia-model-name"
}
```

## 🛠️ Development

### Prerequisites

- Python 3.8+ (for API functions)
- Node.js 18+ (for Vercel CLI)
- Git
- NVIDIA CUDA (optional, for GPU acceleration)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/plturrell/aiqtoolkit-nvidia-ui.git
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run locally**
   ```bash
   # Option 1: Simple HTTP server
   python -m http.server 3000
   
   # Option 2: Vercel CLI
   npm install -g vercel
   vercel dev
   ```

## 🔒 Security

- **CORS Protection**: Configured CORS headers for secure cross-origin requests
- **Environment Variables**: Sensitive data stored securely in environment variables
- **Input Validation**: API inputs are validated and sanitized

## 📈 Performance

- **Serverless Functions**: Auto-scaling based on demand
- **CDN Distribution**: Global edge network via Vercel
- **Optimized Assets**: Compressed images and minified code
- **Design System**: Premium design system for consistent UI performance

## 🤝 Contributing

We welcome contributions! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **NVIDIA**: For providing powerful AI models and infrastructure
- **AIQToolkit Team**: For the foundational framework
- **Vercel**: For serverless hosting infrastructure

---

<div align="center">
  <p>Built with ❤️ by the AIQToolkit Team</p>
</div>