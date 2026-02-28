from fastapi import FastAPI
from pydantic import BaseModel
from backend.agents.manager import run_structurai
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="StructurAI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptRequest(BaseModel):
    prompt: str


@app.get("/")
def home():
    return {"message": "StructurAI is running 🚀"}


@app.post("/generate-ui")
def generate_ui(req: PromptRequest):
    return run_structurai(req.prompt)

app.mount("/generated_projects", StaticFiles(directory="generated_projects"), name="generated_projects")