import os
from fastapi import FastAPI, Response, Request
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from backend.agents.manager import run_structurai

app = FastAPI(title="StructurAI")

# 1. IFRAME PERMISSIONS MIDDLEWARE
# This prevents the "blank screen" by allowing the UI to load in your React iframe
@app.middleware("http")
async def add_frame_options_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Frame-Options"] = "ALLOWALL"
    return response

# 2. UPDATED CORS SETTINGS
# Added your specific Vercel URL from the error log to fix the 'Origin not allowed' issue
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://structur-ai.vercel.app",
        "https://structur-l52itkt8g-sk-karismas-projects.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptRequest(BaseModel):
    prompt: str

@app.get("/")
def home():
    return {"message": "StructurAI Studio is live 🚀"}

@app.post("/generate-ui")
def generate_ui(req: PromptRequest):
    # This calls your AI agent logic
    return run_structurai(req.prompt)

# 3. STATIC FILE SERVING
# Ensures the folder exists and is accessible via URL
os.makedirs("generated_projects", exist_ok=True)
app.mount("/generated_projects", StaticFiles(directory="generated_projects"), name="generated_projects")

# 4. RENDER DYNAMIC PORT
if __name__ == "__main__":
    import uvicorn
    # Render assigns a port dynamically via the PORT environment variable
    port = int(os.getenv("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)