from services.requirement_analyzer import RequirementAnalyzerService
from services.ollama_service import OllamaService
from prompts.requirement_prompt import build_requirement_prompt
from utils.parser import parse_testcases


class SmartTestCaseService:

    def __init__(self):
        self.analyzer = RequirementAnalyzerService()
        self.llm = OllamaService()

    def generate(self, requirement: str):

        # Step 1: Analyze requirement
        analysis = self.analyzer.analyze(requirement)

        # Step 2: Generate test cases (JSON)
        prompt = build_requirement_prompt(analysis)
        response = self.llm.generate(prompt)

        # Step 3: Parse JSON
        testcases = parse_testcases(response)

        return testcases