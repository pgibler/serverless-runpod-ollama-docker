#!/bin/bash

# Start Ollama service in the background
echo "Starting Ollama service..."
ollama serve &

# Wait a moment for Ollama to initialize
sleep 5

# Start the RunPod handler (this will also wait for Ollama to be ready)
echo "Starting RunPod handler..."
python3 /app/handler.py
