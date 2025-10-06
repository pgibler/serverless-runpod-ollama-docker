# serverless-runpod-ollama-docker
A serverless RunPod Ollama Docker container that serves Ollama API requests through HTTPS.

## Overview

This Docker container is designed to run Ollama on RunPod's serverless platform. It includes:
- Ollama server for running LLMs
- RunPod serverless handler for processing API requests
- HTTPS support (handled by RunPod's infrastructure)

## Building the Docker Image

```bash
docker build -t serverless-runpod-ollama .
```

## Running Locally

To test the container locally:

```bash
docker run --gpus all -p 8000:8000 serverless-runpod-ollama
```

## Deploying to RunPod

1. Push your Docker image to a container registry (Docker Hub, GHCR, etc.):
   ```bash
   docker tag serverless-runpod-ollama your-username/serverless-runpod-ollama
   docker push your-username/serverless-runpod-ollama
   ```

2. In RunPod:
   - Go to Serverless → Templates
   - Create a new template
   - Set your container image
   - Configure GPU settings
   - Deploy your endpoint

3. RunPod will automatically handle HTTPS termination and route requests to your container on port 8000.

## API Usage

Send requests to your RunPod endpoint with the following format:

### Example: Generate Text

```json
{
  "input": {
    "method": "POST",
    "endpoint": "/api/generate",
    "data": {
      "model": "llama2",
      "prompt": "Why is the sky blue?",
      "stream": false
    }
  }
}
```

### Example: List Models

```json
{
  "input": {
    "method": "GET",
    "endpoint": "/api/tags"
  }
}
```

### Example: Pull a Model

```json
{
  "input": {
    "method": "POST",
    "endpoint": "/api/pull",
    "data": {
      "name": "llama2"
    }
  }
}
```

## Supported Ollama Endpoints

All Ollama API endpoints are supported:
- `/api/generate` - Generate a completion
- `/api/chat` - Generate a chat completion
- `/api/tags` - List local models
- `/api/pull` - Pull a model from the registry
- `/api/push` - Push a model to the registry
- `/api/create` - Create a model from a Modelfile
- `/api/delete` - Delete a model
- `/api/copy` - Copy a model
- `/api/show` - Show model information

## Environment Variables

- `OLLAMA_URL` - URL of the Ollama service (default: `http://localhost:11434`)

## Notes

- The first request may take longer as Ollama initializes
- Make sure to pull models before using them (use the `/api/pull` endpoint)
- RunPod handles HTTPS termination, so the container runs HTTP internally on port 8000
- GPU support is automatically configured when using RunPod's GPU instances
