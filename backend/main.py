import os
from fastapi import FastAPI, Response, Request
from pydantic import BaseModel
from backend.agents.manager import run_structurai
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="StructurAI")

# 1. ADD IFRAME PERMISSIONS MIDDLEWARE
@app.middleware("http")
async def add_frame_options_header(request: Request, call_next):
    response = await call_next(request)
    # Allows the generated designs to load inside your React workspace iframe
    response.headers["X-Frame-Options"] = "ALLOWALL"
    return response

# 2. UPDATE CORS FOR DEPLOYMENT
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For initial deployment, allow all. Refine to your Vercel URL later.
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
    return run_structurai(req.prompt)

# Ensure the folder exists to prevent mount errors
os.makedirs("generated_projects", exist_ok=True)
app.mount("/generated_projects", StaticFiles(directory="generated_projects"), name="generated_projects")

# 3. DYNAMIC PORT HANDLING
if __name__ == "__main__":
    import uvicorn
    # Render provides a PORT environment variable
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)