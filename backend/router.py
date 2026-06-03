from models.local import (
    is_ollama_running,
    polish_draft,
)


def route_request(
    mode: str,
    draft: str,
    profile: dict,
) -> dict:

    if mode in (
        "referral",
        "sales_networking",
    ):

        if is_ollama_running():

            result = polish_draft(
                draft=draft,
                mode=mode,
            )

            return {
                "draft": result["text"],
                "model_used": "phi3:mini",
                "tokens_used": result["tokens_used"],
            }

        return {
            "draft": draft,
            "model_used": "template_only",
            "tokens_used": 0,
        }

    if mode == "opportunity":

        return {
            "draft": draft,
            "model_used": "pending_gemini",
            "tokens_used": 0,
        }

    return {
        "draft": draft,
        "model_used": "template_only",
        "tokens_used": 0,
    }