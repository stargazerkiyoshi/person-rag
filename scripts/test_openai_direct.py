import json
from pathlib import Path

from openai import OpenAI


def load_config() -> dict:
    path = Path("config/config.json")
    if not path.exists():
        raise FileNotFoundError("config/config.json not found")
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    config = load_config()
    api_key = str(config.get("llm_api_key") or "")
    model = str(config.get("llm_model") or "")
    base_url = str(config.get("llm_base_url") or "")

    if not api_key or not model:
        raise ValueError("llm_api_key/llm_model is missing in config/config.json")

    client = OpenAI(api_key=api_key, base_url=base_url or None)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Reply with a short test message."},
        ],
        temperature=0.2,
    )
    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
