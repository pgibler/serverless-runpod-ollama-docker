FROM nvidia/cuda:12.1.0-base-ubuntu22.04

# Install dependencies
RUN apt-get update && apt-get install -y \
    curl \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Set working directory
WORKDIR /app

# Copy application files
COPY requirements.txt .
COPY handler.py .
COPY start.sh .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Make start script executable
RUN chmod +x start.sh

# Expose port for RunPod handler
EXPOSE 8000

# Start the application
CMD ["/app/start.sh"]
