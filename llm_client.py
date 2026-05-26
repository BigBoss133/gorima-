import os
import requests
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_MODEL = "llama-3.3-70b-versatile"
OLLAMA_MODEL = "llama3.1:8b"
OLLAMA_URL = "http://localhost:11434"

TIMEOUT_SECONDS = 15
OLLAMA_TIMEOUT = 60

FALLBACK_ERROR_MESSAGE = (
    "Mi dispiace, al momento non riesco a elaborare la richiesta. "
    "Groq e il modello locale non sono disponibili. "
    "Riprova tra qualche istante o contatta il supporto tecnico."
)


def query_ollama(system_prompt: str, user_query: str) -> str | None:
    """Query local Ollama instance as emergency fallback."""
    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/chat",
            json={
                "model": OLLAMA_MODEL,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_query},
                ],
                "stream": False,
                "options": {"temperature": 0.7, "num_predict": 512},
            },
            timeout=OLLAMA_TIMEOUT,
        )
        if response.status_code == 200:
            data = response.json()
            content = data.get("message", {}).get("content", "").strip()
            if content:
                return content
        else:
            print(f"[LLM Client] Ollama returned status {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("[LLM Client] Ollama not running or not reachable at localhost:11434")
    except Exception as e:
        print(f"[LLM Client] Ollama error: {e}")
    return None


def query_llm(system_prompt: str, user_query: str) -> str:
    """Query an LLM via Groq → Ollama (local fallback)."""

    if GROQ_API_KEY:
        try:
            client = OpenAI(
                base_url="https://api.groq.com/openai/v1",
                api_key=GROQ_API_KEY,
                timeout=TIMEOUT_SECONDS,
            )
            response = client.chat.completions.create(
                model=GROQ_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_query},
                ],
            )
            content = response.choices[0].message.content
            if content:
                return content.strip()
        except Exception as e:
            print(f"[LLM Client] Groq API error: {e}")
    else:
        print("[LLM Client] GROQ_API_KEY not set, skipping Groq.")

    print("[LLM Client] Falling back to local Ollama...")
    result = query_ollama(system_prompt, user_query)
    if result:
        return result

    return FALLBACK_ERROR_MESSAGE
