import httpx


OLLAMA_BASE_URL = "http://localhost:11434"
LOCAL_MODEL = "phi3:mini"
MAX_TOKENS = 300


SYSTEM_PROMPTS = {
    "referral": (
        "You are editing a LinkedIn referral request. "
        "Fix grammar and make it sound natural and warm. "
        "Do not add new information. "
        "Return only the message text."
    ),
    "sales_networking": (
        "You are editing a LinkedIn networking message. "
        "Make it sound curious and genuine. "
        "Do not add new information. "
        "Return only the message text."
    ),
}


def is_ollama_running() -> bool:
    try:
        response = httpx.get(
            OLLAMA_BASE_URL,
            timeout=2.0,
        )

        return response.status_code == 200

    except Exception:
        return False


def polish_draft(
    draft: str,
    mode: str,
) -> dict:

    system_prompt = SYSTEM_PROMPTS.get(
        mode,
        "Improve the writing. Return only the message text.",
    )

    user_message = f"Edit this message:\n\n{draft}"

    prompt = (
        f"{system_prompt}\n\n"
        f"{user_message}"
    )

    response = httpx.post(
        f"{OLLAMA_BASE_URL}/api/generate",
        json={
            "model": LOCAL_MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_predict": MAX_TOKENS,
            },
        },
        timeout=60.0,
    )

    response.raise_for_status()

    data = response.json()

    return {
        "text": data.get("response", "").strip(),
        "tokens_used": data.get("eval_count", 0),
    }


if __name__ == "__main__":

    print("Checking Ollama...")

    if not is_ollama_running():
        print("Ollama is not running.")
        raise SystemExit(1)

    result = polish_draft(
        draft=(
            "Hi John, I recently applied to Google "
            "and wanted ask if you can refer me."
        ),
        mode="referral",
    )

    print("\nPolished Draft:\n")
    print(result["text"])

    print("\nTokens Used:")
    print(result["tokens_used"])