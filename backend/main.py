from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


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
    title="LinkedIn Messaging Backend",
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
async def save_profile(
    profile: Profile
) -> dict[str, str]:
    return {"status": "not implemented"}


# ------------------------
# Get Cached Profile
# ------------------------

@app.get("/profile/{linkedin_url:path}")
async def get_profile(
    linkedin_url: str
) -> dict[str, str]:
    return {"status": "not implemented"}