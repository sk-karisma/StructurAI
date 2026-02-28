from playwright.sync_api import sync_playwright
import os


def html_to_pdf(html_path):

    pdf_path = html_path.replace(".html", ".pdf")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width":1440, "height":900})

        page.goto(f"file://{os.path.abspath(html_path)}")
        page.wait_for_load_state("networkidle")

        page.pdf(
            path=pdf_path,
            print_background=True,
            width="1440px",
            height="900px"
        )

        browser.close()

    return pdf_path