import os
from backend.agents.requirement_agent import parse_requirements
from backend.services.html_renderer import generate_html
from backend.services.pdf_renderer import html_to_pdf

def run_structurai(prompt: str):
    structured = parse_requirements(prompt)
    if "error" in structured:
        return structured

    html_filename = generate_html(structured)
    local_html_path = os.path.join("generated_projects", html_filename)
    
    # Generate PDF using local file path
    pdf_path = html_to_pdf(local_html_path)

    # Construct Public URL for Frontend Iframe
    preview_url = f"http://127.0.0.1:8000/generated_projects/{html_filename}"

    return {
        "structure": structured,
        "preview_url": preview_url,
        "pdf_file": pdf_path.replace("\\", "/")
    }