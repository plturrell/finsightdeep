# AIQToolkit NVIDIA 🚀

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fplturrell%2Faiqtoolkit-nvidia&env=NVIDIA_ENDPOINT&envDescription=NVIDIA%20Brev%20Endpoint%20URL&envLink=https://brev.nvidia.com&project-name=aiqtoolkit-nvidia)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)
[![NVIDIA Blueprint](https://img.shields.io/badge/NVIDIA-Blueprint-76B900)](https://developer.nvidia.com/)

A powerful, production-ready web interface for NVIDIA AI model integration and report generation, built on the AIQToolkit framework.

## ✨ Features

- **🎯 NVIDIA Integration** - Seamless connection to NVIDIA AI models and services
- **📊 Interactive UI** - Clean, responsive web interface for AI model interaction
- **🖥️ Control Tower** - Real-time monitoring of NVIDIA services and their performance
- **⚡ Serverless Architecture** - Built for Vercel with auto-scaling capabilities
- **🔒 Secure API Proxy** - CORS-enabled API endpoints with environment-based configuration
- **📱 Mobile Responsive** - Works perfectly on desktop, tablet, and mobile devices
- **🚀 One-Click Deploy** - Deploy to Vercel with a single click
- **🔧 Easy Configuration** - Simple environment variable setup
- **🖥️ Local Console** - Try the blueprint from your own launchable console

## 🚀 Quick Start

### Deploy to Vercel (Recommended)

1. Click the "Deploy with Vercel" button above
2. Add your `NVIDIA_ENDPOINT` environment variable
3. Deploy and start using immediately!

### Run Locally with Console Launcher

```bash
# Clone the repository
git clone https://github.com/plturrell/aiqtoolkit-nvidia.git
cd aiqtoolkit-nvidia

# Run with default settings
python scripts/launch_nvidia_blueprint_console.py

# Run with specific ports
python scripts/launch_nvidia_blueprint_console.py --api-port 8000 --ui-port 8080

# Run in interactive console mode
python scripts/launch_nvidia_blueprint_console.py --console

# Run with custom NVIDIA endpoint
python scripts/launch_nvidia_blueprint_console.py --nvidia-endpoint="https://your-endpoint.com"
```

### Local Development

```bash
# Clone the repository
git clone https://github.com/plturrell/aiqtoolkit-nvidia.git
cd aiqtoolkit-nvidia/web-ui

# Start development server
python -m http.server 3000
```

Visit `http://localhost:3000/public/control-tower.html` to see the NVIDIA Control Tower.

## 📡 Monitored NVIDIA Services

The Control Tower UI monitors these NVIDIA services:

- **NVIDIA NIM** - NVIDIA Inference Microservices for custom model deployment
- **NVIDIA API** - NVIDIA AI Foundation Models API for standardized access
- **NVIDIA NeMo** - NVIDIA NeMo text generation service
- **NVIDIA Triton** - NVIDIA Triton Inference Server for high-performance serving

## 📁 Project Structure

```
web-ui/
├── public/             # Static web files
│   ├── control-tower.html  # Main control tower interface
│   ├── index.html      # Home page
│   └── ...             # Other UI pages
├── api/                # API handlers
│   ├── generate.py     # Text generation API
│   ├── health.py       # Health check API
│   ├── nvidia.py       # NVIDIA services API
│   └── reasoning.py    # Reasoning system API
├── auto_deploy.sh      # Automated deployment script
├── deploy_vercel.html  # Vercel deployment helper
└── vercel.json         # Vercel configuration
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

### Health Check
```http
GET /api/health
```

### Generate with NVIDIA
```http
POST /api/generate
Content-Type: application/json

{
  "prompt": "Your AI prompt here",
  "model": "nvidia-model-name"
}
```

### NVIDIA Service Access
```http
POST /api/nvidia
Content-Type: application/json

{
  "prompt": "Your prompt here",
  "service_type": "nim|api|nemo|triton",
  "model": "model-name"
}
```

## 🖥️ Using the Console Launcher

The `launch_nvidia_blueprint_console.py` script provides a simple way to run the NVIDIA Blueprint locally:

```bash
python scripts/launch_nvidia_blueprint_console.py --console
```

Console commands:
- `status` - Check service status
- `test` - Test NVIDIA services
- `open` - Open Control Tower in browser
- `logs` - View service logs
- `config` - Show current configuration
- `restart` - Restart services
- `quit` - Exit the console

## 🛠️ Development

### Prerequisites

- Python 3.8+ (for API functions)
- Git
- NVIDIA CUDA (optional, for GPU acceleration)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/plturrell/aiqtoolkit-nvidia.git
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run locally**
   ```bash
   # Option 1: Simple HTTP server
   python -m http.server 3000
   
   # Option 2: Console launcher
   python scripts/launch_nvidia_blueprint_console.py
   ```

## 🚢 Deployment

### Automated Deployment

Use the included deployment script:

```bash
chmod +x auto_deploy.sh
./auto_deploy.sh
```

### Manual Deployment

1. **Deploy to Vercel:**
   ```bash
   vercel --prod
   ```

2. **Set environment variables:**
   ```bash
   vercel env add NVIDIA_ENDPOINT production
   ```

## 🔒 Security

- **CORS Protection**: Configured CORS headers for secure cross-origin requests
- **Environment Variables**: Sensitive data stored securely in environment variables
- **Input Validation**: API inputs are validated and sanitized

## 📈 Performance

- **Serverless Functions**: Auto-scaling based on demand
- **CDN Distribution**: Global edge network via Vercel
- **Optimized Assets**: Compressed images and minified code
- **GPU Optimization**: NVIDIA-specific optimizations when available

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md).

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: [AIQToolkit Docs](https://docs.aiqtoolkit.ai)
- **Issues**: [GitHub Issues](https://github.com/plturrell/aiqtoolkit-nvidia/issues)

## 🙏 Acknowledgments

- **NVIDIA**: For providing powerful AI models and infrastructure
- **AIQToolkit Team**: For the foundational framework

---

<div align="center">
  <p>Built with ❤️ by the AIQToolkit Team</p>
</div>