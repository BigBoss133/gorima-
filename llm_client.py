import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

GROQ_MODEL = "llama-3.3-70b-versatile"
OPENROUTER_MODEL = "deepseek/deepseek-v4-flash:free"

TIMEOUT_SECONDS = 15

FALLBACK_ERROR_MESSAGE = (
    "Mi dispiace, al momento non riesco a elaborare la richiesta. "
    "Entrambi i servizi LLM (Groq e OpenRouter) non sono disponibili. "
    "Riprova tra qualche istante o contatta il supporto tecnico."
)


def query_llm(system_prompt: str, user_query: str) -> str:
    """Query an LLM via Groq (primary) or OpenRouter (fallback)."""

    # Try Groq first
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

    # Fallback to OpenRouter
    if OPENROUTER_API_KEY:
        try:
            client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=OPENROUTER_API_KEY,
                timeout=TIMEOUT_SECONDS,
            )
            response = client.chat.completions.create(
                model=OPENROUTER_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_query},
                ],
            )
            content = response.choices[0].message.content
            if content:
                return content.strip()
        except Exception as e:
            print(f"[LLM Client] OpenRouter API error: {e}")
    else:
        print("[LLM Client] OPENROUTER_API_KEY not set, skipping OpenRouter.")

    return FALLBACK_ERROR_MESSAGE
