import os
from fastapi import FastAPI, Response, Request
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from backend.agents.manager import run_structurai

app = FastAPI(title="StructurAI Studio")

# 1. IFRAME PERMISSIONS MIDDLEWARE
# Allows the generated HTML to render inside the React Workspace
@app.middleware("http")
async def add_frame_options_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Frame-Options"] = "ALLOWALL"
    return response

# 2. EMERGENCY CORS FIX
# Using "*" allows ALL origins (Vercel, Localhost, etc.) to talk to this API.
# This fixes the "Origin not allowed" error seen in your console logs.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptRequest(BaseModel):
    prompt: str

# 3. HEALTH CHECK ROUTE
# Visit https://structurai.onrender.com/ to see if this returns successfully.
@app.get("/")
def home():
    return {
        "status": "online",
        "message": "StructurAI Studio Backend is live 🚀",
        "environment": os.getenv("RENDER", "local")
    }

# 4. CORE AI GENERATION ROUTE
@app.post("/generate-ui")
def generate_ui(req: PromptRequest):
    try:
        return run_structurai(req.prompt)
    except Exception as e:
        # This will return the actual error message to your browser console
        return {"error": str(e), "detail": "Check Render logs for full traceback"}

# 5. STATIC STORAGE SETUP
# Mounts the 'generated_projects' folder so the iframe can load the .html files.
os.makedirs("generated_projects", exist_ok=True)
app.mount("/generated_projects", StaticFiles(directory="generated_projects"), name="generated_projects")

# 6. DYNAMIC PORT FOR RENDER
if __name__ == "__main__":
    import uvicorn
    # Render assigns a port via the PORT environment variable (defaulting to 10000)
    port = int(os.getenv("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)