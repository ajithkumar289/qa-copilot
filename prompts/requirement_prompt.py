def build_requirement_prompt(requirement: str):

    return f"""
You are a Senior QA Engineer.

Generate:

1. Positive Test Cases
2. Negative Test Cases
3. Edge Cases
4. Security Test Cases

Requirement:
{requirement}

For every test case include:

- Test Case ID
- Title
- Steps
- Expected Result

Return the answer in Markdown.
"""