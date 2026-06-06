import os

import httpx
from dotenv import load_dotenv


load_dotenv()


GEMINI_MODEL = "gemini-2.5-flash"
MAX_OUTPUT_TOKENS = 100

API_KEY = os.getenv("GEMINI_API_KEY")


def is_gemini_configured() -> bool:
    return bool(API_KEY and API_KEY.strip())


def get_focus_area(company: str) -> dict:

    if not is_gemini_configured():
        raise RuntimeError("GEMINI_API_KEY is not configured")

    url = (
        "https://generativelanguage.googleapis.com/"
        f"v1beta/models/{GEMINI_MODEL}:generateContent"
        f"?key={API_KEY}"
    )

    prompt = (
        f"In one phrase (max 6 words), what does "
        f"{company}'s engineering team primarily work on "
        f"— is it more C++ or systems programming, "
        f"or cloud infrastructure and DevOps? "
        f"Reply with only the phrase, nothing else."
    )

    response = httpx.post(
        url,
        json={
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ],
            # "tools": [
            #     {
            #         "google_search": {}
            #     }
            # ],
            "generationConfig": {
                "maxOutputTokens": MAX_OUTPUT_TOKENS
            },
        },
        timeout=30.0,
    )

    response.raise_for_status()

    data = response.json()

    text = (
        data["candidates"][0]
        ["content"]["parts"][0]
        ["text"]
        .strip()
    )

    token_count = (
        data.get("usageMetadata", {})
        .get("totalTokenCount", 0)
    )

    return {
        "focus_area": text,
        "tokens_used": token_count,
    }


if __name__ == "__main__":

    if not is_gemini_configured():
        print("GEMINI_API_KEY not configured")
        raise SystemExit(1)

    result = get_focus_area("Google")

    print("Focus Area:")
    print(result["focus_area"])

    print("\nTokens Used:")
    print(result["tokens_used"])