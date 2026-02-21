"""
Ollama Client
Python client to interact with Ollama locally for LLM inference
"""

import requests
from typing import Optional
from backend.app.config import OLLAMA_BASE_URL, OLLAMA_MODEL


# Default timeout for requests (in seconds)
DEFAULT_TIMEOUT = 120


def generate_response(prompt: str, model: Optional[str] = None, timeout: int = DEFAULT_TIMEOUT) -> str:
    """
    Generate a response from Ollama LLM.

    Args:
        prompt: The input prompt to send to the LLM
        model: The model to use (defaults to OLLAMA_MODEL from config)
        timeout: Request timeout in seconds

    Returns:
        The generated response text from the LLM

    Raises:
        requests.RequestException: If the request fails
        ValueError: If the response is invalid
    """
    model = model or OLLAMA_MODEL
    
    url = f"{OLLAMA_BASE_URL}/api/generate"
    
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    
    try:
        response = requests.post(url, json=payload, timeout=timeout)
        response.raise_for_status()
        
        data = response.json()
        
        if "response" not in data:
            raise ValueError("Invalid response: missing 'response' field")
        
        return data["response"]
        
    except requests.exceptions.Timeout:
        raise requests.RequestException(f"Request timed out after {timeout} seconds")
    except requests.exceptions.ConnectionError:
        raise requests.RequestException(f"Failed to connect to Ollama at {OLLAMA_BASE_URL}")
    except requests.exceptions.HTTPError as e:
        raise requests.RequestException(f"HTTP error: {e}")
    except ValueError as e:
        raise ValueError(f"Invalid response format: {e}")
    except Exception as e:
        raise requests.RequestException(f"Unexpected error: {e}")
