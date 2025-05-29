# AIQToolkit NVIDIA Blueprint Launcher Guide

This document provides instructions for launching the AIQToolkit NVIDIA Blueprint through GitHub or other platforms.

## Runtime Requirements

The AIQToolkit NVIDIA Blueprint requires the following runtime environment:

- Python 3.8+
- CUDA 11.8+ (for GPU acceleration, optional)
- NVIDIA drivers (for GPU acceleration, optional)
- Git

## Launch Options

### 1. Launch with GitHub Codespaces

The fastest way to get started:

1. Visit the [AIQToolkit NVIDIA repository](https://github.com/plturrell/aiqtoolkit-nvidia)
2. Click "Code" > "Open with Codespaces"
3. Once the environment is ready, run:
   ```bash
   cd web-ui
   python -m http.server 8080 --directory public &
   python -m http.server 8000 --directory api &
   ```
4. Open the forwarded port 8080 in your browser

### 2. Launch with Jupyter Notebook

For a guided experience:

1. Open the `launch.ipynb` notebook in Jupyter, Google Colab, or any notebook environment
2. Follow the step-by-step instructions in the notebook
3. The notebook will set up the environment and launch the blueprint

### 3. Launch with Docker

For a containerized deployment:

```bash
# Build the container
docker build -t aiqtoolkit-nvidia .

# Run with NVIDIA GPU support
docker run --gpus all -p 8000:8000 -p 8080:8080 -e NVIDIA_API_KEY=your_api_key aiqtoolkit-nvidia

# Or run CPU-only version
docker run -p 8000:8000 -p 8080:8080 -e NVIDIA_API_KEY=your_api_key aiqtoolkit-nvidia
```

### 4. Launch with Console Script

For a command-line interface:

```bash
# Run with default settings
python scripts/launch_nvidia_blueprint_console.py

# Run with specific configuration
python scripts/launch_nvidia_blueprint_console.py --nvidia-api-key=your_api_key --nvidia-endpoint=your_endpoint
```

## NVIDIA API Key (Optional)

To use NVIDIA AI services, you can provide an API key:

1. Get an API key from [NVIDIA Developer Portal](https://developer.nvidia.com/)
2. Set it as an environment variable:
   ```bash
   export NVIDIA_API_KEY=your_api_key
   ```
3. Or provide it directly to the launch script:
   ```bash
   python scripts/launch_nvidia_blueprint_console.py --nvidia-api-key=your_api_key
   ```

## Using GPU Acceleration

The blueprint can use NVIDIA GPUs for accelerated performance:

1. Ensure NVIDIA drivers are installed
2. Verify GPU availability with `nvidia-smi`
3. Launch with GPU options:
   ```bash
   python scripts/launch_nvidia_blueprint_console.py --gpu-count=1 --enable-flash-attn --enable-tensorrt
   ```

## Troubleshooting

If you encounter issues launching the blueprint:

1. Check that all prerequisites are installed
2. Ensure ports 8000 and 8080 are available
3. Check GPU drivers are properly installed (for GPU acceleration)
4. Verify network connectivity for NVIDIA service access

For more help, see the full documentation in the repository README.md file.

## Security Notes

- The blueprint does not store or transmit your NVIDIA API key outside your environment
- All API calls to NVIDIA services are made directly from your environment
- No user data is collected or shared with external services