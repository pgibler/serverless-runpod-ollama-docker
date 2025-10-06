import runpod
import requests
import json
import time
import os

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")

def wait_for_ollama(max_retries=30, delay=2):
    """Wait for Ollama service to be ready."""
    for i in range(max_retries):
        try:
            response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
            if response.status_code == 200:
                print("Ollama service is ready")
                return True
        except requests.exceptions.RequestException:
            pass
        
        if i < max_retries - 1:
            print(f"Waiting for Ollama service... (attempt {i + 1}/{max_retries})")
            time.sleep(delay)
    
    return False

def handler(job):
    """
    Handler function for RunPod serverless.
    Proxies requests to Ollama API.
    
    Expected input format:
    {
        "input": {
            "method": "POST",
            "endpoint": "/api/generate",
            "data": {
                "model": "llama2",
                "prompt": "Hello, world!",
                "stream": false
            }
        }
    }
    """
    job_input = job.get("input", {})
    
    # Extract request parameters
    method = job_input.get("method", "POST").upper()
    endpoint = job_input.get("endpoint", "/api/generate")
    data = job_input.get("data", {})
    
    # Ensure endpoint starts with /
    if not endpoint.startswith("/"):
        endpoint = "/" + endpoint
    
    # Build full URL
    url = f"{OLLAMA_URL}{endpoint}"
    
    try:
        # Make request to Ollama
        if method == "GET":
            response = requests.get(url, timeout=300)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=300)
        elif method == "DELETE":
            response = requests.delete(url, json=data, timeout=300)
        else:
            return {"error": f"Unsupported HTTP method: {method}"}
        
        # Return response
        try:
            response_data = response.json()
        except json.JSONDecodeError:
            response_data = {"text": response.text}
        
        return {
            "status_code": response.status_code,
            "response": response_data
        }
        
    except requests.exceptions.Timeout:
        return {"error": "Request to Ollama timed out"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

if __name__ == "__main__":
    print("Starting RunPod handler...")
    
    # Wait for Ollama to be ready
    if not wait_for_ollama():
        print("ERROR: Ollama service failed to start")
        exit(1)
    
    print("Starting RunPod serverless handler")
    runpod.serverless.start({"handler": handler})
