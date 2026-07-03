def build_analyzer_prompt(requirement: str) -> str:
    return f"""
You are a Senior QA Architect.

Analyze the requirement and return STRICTLY structured output:

### 1. Requirement Summary
Short summary of what system should do.

### 2. Functional Requirements
List all functional requirements as FR-001, FR-002 format.

### 3. Business Rules
All rules like validations, limits, conditions.

### 4. Assumptions
Any assumed behavior not mentioned.

### 5. Missing Requirements
What is NOT specified but needed.

### 6. Risks
Technical + business risks.

### 7. Test Design Inputs
Key points a QA engineer should consider before writing test cases.

Requirement:
{requirement}

IMPORTANT:
Keep output structured and clear for another AI system to consume.
"""