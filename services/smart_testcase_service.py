from services.requirement_analyzer import RequirementAnalyzerService
from services.ollama_service import OllamaService
from prompts.requirement_prompt import build_requirement_prompt


class SmartTestCaseService:

    def __init__(self):
        self.analyzer = RequirementAnalyzerService()
        self.llm = OllamaService()

    def generate(self, requirement: str):

        # Step 1: Get analysis first
        analysis = self.analyzer.analyze(requirement)

        # Step 2: Convert analysis into test cases
        prompt = build_requirement_prompt(analysis)

        return self.llm.generate(prompt)