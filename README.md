# StructurAI Studio

Transform thoughts into interfaces instantly.

StructurAI Studio is an AI-powered full-stack application that converts natural language prompts into modern, styled UI layouts with live preview and PDF export.

---

## Overview

StructurAI Studio allows users to:

- Enter a natural language UI description  
- Automatically generate structured UI layouts  
- Preview generated UI live inside the app  
- Export UI as a PDF  
- Maintain version history  

The system integrates LLM-based requirement parsing with dynamic HTML generation and cloud deployment.

---

## Architecture

### Frontend
- React (Single Page App)
- Dynamic UI generation
- Live iframe preview
- Version tracking
- API integration with backend

### Backend
- FastAPI
- Gemini API (LLM requirement parsing)
- Jinja2 template rendering
- Playwright for PDF generation
- Static file serving for generated projects

---

## Tech Stack

### Frontend
- React
- Fetch API
- Inline styling (custom UI)
- Vercel deployment

### Backend
- FastAPI
- Google Gemini API
- Jinja2
- Playwright (Chromium)
- Uvicorn
- Render deployment

---

## Multi-Agent Architecture

StructurAI Studio is built using a modular **Multi-Agent System**, where each agent is responsible for a specific stage in the UI generation pipeline.

### Agents Overview

#### 1️⃣ Requirement Agent
- Parses natural language prompts using Gemini API
- Extracts:
  - Page name
  - Layout type
  - Sections
  - Components
- Converts unstructured input into structured JSON schema

#### 2️⃣ Layout Agent
- Refines UI structure
- Determines layout hierarchy and section arrangement
- Enhances structural consistency

#### 3️⃣ Validator Agent
- Validates generated structure
- Ensures required fields exist
- Prevents malformed UI schemas
- Provides safe fallback responses

#### 4️⃣ Manager Agent (Orchestrator)
- Coordinates all agents
- Executes pipeline sequentially:
  - Requirement → Layout → Validation
- Passes final structure to rendering services
- Returns structured preview response

---

## Execution Flow

User Prompt  
⬇  
Requirement Agent (LLM parsing)  
⬇  
Layout Agent (Structure refinement)  
⬇  
Validator Agent (Schema validation)  
⬇  
Manager Agent (Pipeline orchestration)  
⬇  
HTML Renderer (Jinja2)  
⬇  
PDF Renderer (Playwright)  
⬇  
Preview URL returned to Frontend  

---

## Why Multi-Agent?

This architecture provides:

- Modular design
- Separation of concerns
- Scalable pipeline
- Easier debugging
- Extensible AI workflow
- Production-ready orchestration pattern

## How It Works

1. User enters a UI prompt
2. Frontend sends POST request to `/generate-ui`
3. Backend:
   - Parses requirements using Gemini
   - Generates structured UI data
   - Renders HTML using Jinja2
   - Converts HTML to PDF using Playwright
4. Backend returns preview URL
5. Frontend loads generated HTML inside iframe

---

## Future Improvements

- Authentication & user accounts
- UI editing mode
- Drag-and-drop component refinement
- Save to database instead of filesystem
- Multi-theme generation
- AI layout refinement agent
