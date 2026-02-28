# main.py

import os
import traceback
from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from backend.agents.manager import run_structurai
from google.genai.errors import ClientError  # Gemini error handling

app = FastAPI(title="StructurAI Studio")


# -----------------------------
# CORS (Safe for Vercel)
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------
# Allow iframe embedding
# -----------------------------
@app.middleware("http")
async def add_frame_options_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Frame-Options"] = "ALLOWALL"
    return response


class PromptRequest(BaseModel):
    prompt: str


# -----------------------------
# Health Check
# -----------------------------
@app.get("/")
def home():
    return {
        "status": "online",
        "message": "StructurAI Studio Backend is live 🚀",
        "environment": os.getenv("RENDER", "local")
    }


# -----------------------------
# Core Generation Route (SYNC)
# -----------------------------
@app.post("/generate-ui")
def generate_ui(req: PromptRequest):
    try:
        result = run_structurai(req.prompt)

        # Normalize return format
        if isinstance(result, dict):
            preview_url = result.get("preview_url") or result.get("url")
        else:
            preview_url = result

        if not preview_url:
            return {
                "error": "No preview URL generated",
                "detail": "run_structurai did not return expected format"
            }

        # Ensure correct static path
        if not preview_url.startswith("/generated_projects"):
            preview_url = f"/generated_projects/{preview_url}"

        return {"preview_url": preview_url}

    # Proper Gemini quota handling
    except ClientError as e:
        error_text = str(e)

        if "429" in error_text or "RESOURCE_EXHAUSTED" in error_text:
            return {
                "error": "Gemini quota exceeded",
                "detail": "Daily free quota reached. Please try again tomorrow or upgrade your plan."
            }

        return {
            "error": "Gemini API error",
            "detail": error_text
        }

    # Generic fallback
    except Exception as e:
        print("ERROR IN generate_ui:")
        traceback.print_exc()
        return {
            "error": "Internal server error",
            "detail": str(e)
        }


# -----------------------------
# Static Folder
# -----------------------------
os.makedirs("generated_projects", exist_ok=True)

app.mount(
    "/generated_projects",
    StaticFiles(directory="generated_projects"),
    name="generated_projects"
)


# -----------------------------
# Render Port Config
# -----------------------------
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 10000))
    print(f"🚀 Starting server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)