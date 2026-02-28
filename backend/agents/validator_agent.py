def validate_code(code: str):

    issues = []

    if "export default" not in code:
        issues.append("Missing default export")

    if "className" not in code:
        issues.append("Tailwind classes missing")

    return {
        "status": "valid" if not issues else "needs_review",
        "issues": issues
    }