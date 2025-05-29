FROM nvidia/cuda:12.1.0-runtime-ubuntu22.04

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    python3 \
    python3-pip \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV NVIDIA_ENDPOINT="https://jupyter0-s1ondnjfx.brevlab.com"

# Expose ports
EXPOSE 8000
EXPOSE 8080

# Start the application
CMD ["bash", "-c", "python3 -m http.server 8000 --directory /app/api & python3 -m http.server 8080 --directory /app/public"]