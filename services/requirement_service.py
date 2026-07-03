from prompts.requirement_prompt import build_requirement_prompt
from services.ollama_service import OllamaService


class RequirementService:

    def __init__(self):

        self.ollama = OllamaService()

    def generate_test_cases(self, requirement):

        prompt = build_requirement_prompt(requirement)

        return self.ollama.generate(prompt)