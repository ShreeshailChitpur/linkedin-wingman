from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from urllib.parse import unquote

import db
from fastapi import HTTPException

import template_engine

import router

from models.local import is_ollama_running
from models.gemini import is_gemini_configured

# ------------------------
# Pydantic Models
# ------------------------

class Profile(BaseModel):
    linkedin_url: str
    name: str
    current_company: str
    current_role: str
    past_companies: list[str]
    education: list[str]
    raw_text: Optional[str] = None


class GenerateRequest(BaseModel):
    mode: str
    profile: Profile
    template_key: str


class GenerateResponse(BaseModel):
    draft: str
    model_used: str
    tokens_used: Optional[int] = None


# ------------------------
# FastAPI App
# ------------------------

app = FastAPI(
    title="LinkedIn Wingman Backend",
    version="0.1.0"
)


# ------------------------
# CORS
# ------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ------------------------
# Health Check
# ------------------------

@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "healthy"}

# ------------------------
# Status Check
# ------------------------

@app.get("/status")
async def status() -> dict:

    try:
        db.list_profiles()
        db_ok = True
    except Exception:
        db_ok = False

    return {
        "ollama": is_ollama_running(),
        "gemini": is_gemini_configured(),
        "templates": template_engine.list_templates(),
        "db": db_ok,
    }


# ------------------------
# Generate Draft
# ------------------------

@app.post(
    "/generate",
    response_model=GenerateResponse,
)
async def generate_message(
    request: GenerateRequest,
) -> GenerateResponse:
    
    try:

        template = template_engine.load_template(
            request.template_key
        )

        profile = request.profile

        slot_values = {
            "name": profile.name,
            "company": profile.current_company,
            "role": profile.current_role,
            "their_background": profile.current_role,
            "focus_area": "C++ and cloud/DevOps",
        }

        draft = template_engine.fill_slots(
            template,
            slot_values,
        )

        result = router.route_request(
            mode = request.mode,
            draft = draft,
            profile= profile.model_dump(),
        )

        return GenerateResponse(
            draft=result["draft"],
            model_used=result["model_used"],
            tokens_used=result["tokens_used"],
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


# ------------------------
# Save Profile
# ------------------------

@app.post("/save-profile")
async def save_profile_endpoint(
    profile: Profile,
) -> dict[str, str]:

    db.save_profile(profile.model_dump())

    return {"status": "saved"}


# ------------------------
# Get Cached Profile
# ------------------------

@app.get("/profile/{linkedin_url:path}")
async def get_profile_endpoint(
    linkedin_url: str,
) -> dict:

    decoded_url = unquote(linkedin_url)

    profile = db.get_profile(decoded_url)

    if profile is None:
        raise HTTPException(
            status_code=404,
            detail="Profile not found",
        )

    return profile

# ------------------------
# Get Templates
# ------------------------

@app.get("/templates")
async def get_templates() -> list[str]:
    return template_engine.list_templates()