import requests

from config import (
    OLLAMA_URL,
    MODEL_NAME,
    REQUEST_TIMEOUT
)


class OllamaService:

    def generate(self, prompt):

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False
            },
            timeout=REQUEST_TIMEOUT
        )

        response.raise_for_status()

        return response.json()["response"]