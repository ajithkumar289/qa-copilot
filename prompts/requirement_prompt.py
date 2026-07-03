def build_requirement_prompt(requirement_analysis: str) -> str:
    return f"""
You are a Senior QA Engineer.

You are given a REQUIREMENT ANALYSIS from a QA Architect.

Your job is to generate HIGH QUALITY test cases based on it.

Include:

- Positive Test Cases
- Negative Test Cases
- Edge Cases
- Security Test Cases

Each test case must include:
- Test Case ID
- Title
- Steps
- Expected Result
- Priority (High/Medium/Low)

Requirement Analysis:
{requirement_analysis}

IMPORTANT:
Focus on missing risks and business rules while creating test cases.
Avoid generic test cases.
"""