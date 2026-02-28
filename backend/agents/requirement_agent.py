import json
import re
from backend.services.gemini_client import generate_json
from backend.schemas.ui_schema import UIStructure

def parse_requirements(prompt: str):
    """
    Converts natural language prompt into validated UI structure JSON.
    """

    system_prompt = """
    You are a UI structure generator.

    Return ONLY valid JSON.
    No explanation.
    No markdown.
    No backticks.
    No extra text.

    Strict format:

    {
      "page_name": "",
      "layout_type": "",
      "sections": [
        {
          "name": "",
          "purpose": "",
          "components_in_section": [
            {
              "type": "",
              "purpose": ""
            }
          ]
        }
      ],
      "components": [
        {
          "type": "",
          "purpose": ""
        }
      ]
    }
    """

    full_prompt = system_prompt + "\n\nUser Input:\n" + prompt

    raw = generate_json(full_prompt)

    try:
        cleaned = raw.strip()

        # Remove markdown code blocks if present
        cleaned = re.sub(r"```json", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"```", "", cleaned)
        cleaned = cleaned.strip()

        # Extract JSON object using regex (safer)
        json_match = re.search(r"\{.*\}", cleaned, re.DOTALL)

        if not json_match:
            raise ValueError("No JSON object found in model response.")

        json_string = json_match.group(0)

        parsed = json.loads(json_string)

        # Validate using Pydantic schema
        validated = UIStructure(**parsed)

        return validated.model_dump()

    except Exception as e:
        return {
            "error": "Invalid model response",
            "details": str(e),
            "raw_output": raw
        }