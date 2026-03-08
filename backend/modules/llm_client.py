import requests, os

OLLAMA_BASE = os.getenv("OLLAMA_BASE_URL","http://localhost:11434")

MODEL_MAP = {
    "math":    "mathstral:latest",
    "general": "gemma:2b",
    "code":    "deepseek-coder:latest",
    "default": "stablelm2:latest",
}

def get_model(subject: str = "default") -> str:
    return MODEL_MAP.get(subject.lower(), MODEL_MAP["default"])

def generate(prompt: str, subject: str = "default", system: str ="") -> str:
    model = get_model(subject)
    payload = {
        "model": model,
        "prompt": prompt,
        "system": system,
        "stream": False,
    }
    try:
        resp = requests.post(f"{OLLAMA_BASE}/api/generate", json=payload, timeout=120)
        resp.raise_for_status()
        return resp.json().get("response", "")
    except requests.exceptions.ConnectionError:
        raise RuntimeError(
            f"Cannot reach Ollama at {OLLAMA_BASE}. "
            "Make sure `ollama serve` is running locally."
        )

def list_models() -> list[str]:
    try:
        resp = requests.get(f"{OLLAMA_BASE}/api/tags", timeout=10)
        resp.raise_for_status()
        return [m["name"] for m in resp.json().get("models", [])]
    except Exception:
        return []
