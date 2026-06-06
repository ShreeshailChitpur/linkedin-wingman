from models.local import (
    is_ollama_running,
    polish_draft,
)

from models.gemini import (
    get_focus_area,
    is_gemini_configured,
)

import template_engine


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

        template = template_engine.load_template(
            "opportunity"
        )

        if is_gemini_configured():

            focus_result = get_focus_area(
                profile["current_company"]
            )

            filled_draft = (
                template_engine.fill_slots(
                    template,
                    {
                        "name": profile["name"],
                        "company": profile["current_company"],
                        "focus_area": focus_result[
                            "focus_area"
                        ],
                    },
                )
            )

            return {
                "draft": filled_draft,
                "model_used": "gemini-2.0-flash",
                "tokens_used": focus_result[
                    "tokens_used"
                ],
            }

        filled_draft = (
            template_engine.fill_slots(
                template,
                {
                    "name": profile["name"],
                    "company": profile["current_company"],
                    "focus_area": (
                        "C++ and cloud/DevOps"
                    ),
                },
            )
        )

        return {
            "draft": filled_draft,
            "model_used": "template_only",
            "tokens_used": 0,
        }

    return {
        "draft": draft,
        "model_used": "template_only",
        "tokens_used": 0,
    }