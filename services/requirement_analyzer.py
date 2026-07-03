from prompts.analyzer_prompt import build_analyzer_prompt
from services.ollama_service import OllamaService


class RequirementAnalyzerService:

    def __init__(self):
        self.ollama = OllamaService()

    def analyze(self, requirement: str):
        prompt = build_analyzer_prompt(requirement)
        return self.ollama.generate(prompt)