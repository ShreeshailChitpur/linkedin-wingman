from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from urllib.parse import unquote

import db
from fastapi import HTTPException


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
# Generate Draft
# ------------------------

@app.post("/generate", response_model=GenerateResponse)
async def generate_message(
    request: GenerateRequest
) -> GenerateResponse:
    return GenerateResponse(
        draft="not implemented",
        model_used="none"
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