from app.providers.llm_provider import LLMProvider

class MockProvider(LLMProvider):
    def name(self) -> str:
        return "mock"

    def chat(self, prompt: str) -> str:
        return f"echo: {prompt}"