import json
from pathlib import Path

import httpx


def load_config() -> dict:
    path = Path("config/config.json")
    if not path.exists():
        raise FileNotFoundError("config/config.json not found")
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    config = load_config()
    base_url = str(config.get("llm_base_url") or "").rstrip("/")
    api_key = str(config.get("llm_api_key") or "")
    model = str(config.get("llm_model") or "")

    if not base_url or not api_key or not model:
        raise ValueError("llm_base_url/llm_api_key/llm_model is missing in config/config.json")

    url = f"{base_url}/chat/completions"
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Reply with a short test message."},
        ],
        "temperature": 0.2,
    }
    headers = {"Authorization": f"Bearer {api_key}"}

    with httpx.Client(timeout=30) as client:
        response = client.post(url, headers=headers, json=payload)

    print(f"status: {response.status_code}")
    try:
        data = response.json()
        print(json.dumps(data, ensure_ascii=False, indent=2)[:1000])
    except json.JSONDecodeError:
        print(response.text[:1000])


if __name__ == "__main__":
    main()
