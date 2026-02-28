import os
import shutil
from datetime import datetime


def create_project_folder(code: str, project_name: str):

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    folder_name = f"{project_name}_{timestamp}"
    project_path = os.path.join("generated_projects", folder_name)

    os.makedirs(project_path, exist_ok=True)
    os.makedirs(os.path.join(project_path, "src"), exist_ok=True)

    # Write React file
    with open(os.path.join(project_path, "src", "App.jsx"), "w") as f:
        f.write(code)

    # Minimal package.json
    with open(os.path.join(project_path, "package.json"), "w") as f:
        f.write("""
{
  "name": "structurai-generated",
  "version": "1.0.0",
  "dependencies": {
    "react": "^18.0.0",
    "react-dom": "^18.0.0"
  }
}
""")

    zip_path = shutil.make_archive(project_path, 'zip', project_path)

    return zip_path