import requests


def analyze_with_groq(api_key: str, model: str, prompt: str) -> str:
    """Call Groq API and return response text."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 1024
    }
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=60
    )
    if response.status_code == 401:
        raise ValueError("invalid_api_key: Check your Groq API key.")
    if response.status_code == 429:
        raise RuntimeError("rate_limit: Too many requests. Wait 30 seconds.")
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]
