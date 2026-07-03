def build_requirement_prompt(requirement_analysis: str) -> str:
    return f"""
You are a Senior QA Engineer.

Convert the following requirement analysis into STRICT JSON format.

IMPORTANT RULES:
- Return ONLY valid JSON
- No markdown
- No explanations
- No extra text

JSON FORMAT:

[
  {{
    "test_case_id": "TC001",
    "title": "string",
    "category": "Positive | Negative | Edge | Security",
    "priority": "High | Medium | Low",
    "steps": [
      "step 1",
      "step 2"
    ],
    "expected_result": "string"
  }}
]

Requirement Analysis:
{requirement_analysis}
"""