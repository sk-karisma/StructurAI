# backend/services/pdf_renderer.py

import os
from playwright.sync_api import sync_playwright


def html_to_pdf(html_path: str):
    # Ensure absolute path
    html_path = os.path.abspath(html_path)

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage"
            ]
        )

        page = browser.new_page()

        page.goto(f"file://{html_path}")

        pdf_path = html_path.replace(".html", ".pdf")

        page.pdf(
            path=pdf_path,
            format="A4",
            print_background=True
        )

        browser.close()

        return pdf_path