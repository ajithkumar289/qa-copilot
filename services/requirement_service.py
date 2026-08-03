from prompts.requirement_prompt import build_requirement_prompt
from services.ollama_service import OllamaService


class RequirementService:

    def __init__(self):

        self.ollama = OllamaService()

    # -------------------------
    # Existing Feature
    # -------------------------

    def generate_test_cases(self, requirement):

        prompt = build_requirement_prompt(requirement)

        return self.ollama.generate(prompt)

    # -------------------------
    # Sprint 6 - Chat with BRD
    # -------------------------

    def answer_from_context(self, context, question):

        prompt = f"""
You are an experienced QA Business Analyst.

Answer ONLY using the information provided in the context.

If the answer cannot be found in the context, reply exactly:

"I couldn't find that information in the uploaded BRD."

----------------------------
Context
----------------------------

{context}

----------------------------
Question
----------------------------

{question}

----------------------------
Answer
----------------------------
"""

        return self.ollama.generate(prompt)