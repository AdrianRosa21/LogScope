from agent.config import AgentConfig

class BaseLLMAdapter:
    def generate(self, prompt: str) -> str:
        raise NotImplementedError

class MockLLMAdapter(BaseLLMAdapter):
    def generate(self, prompt: str) -> str:
        return "Resumen generado por IA simulada: Se han revisado los logs determinísticamente y se han extraído los hechos, inferencias y recomendaciones."

def get_llm_adapter() -> BaseLLMAdapter:
    if AgentConfig.LLM_PROVIDER == "mock":
        return MockLLMAdapter()
    
    if AgentConfig.LLM_PROVIDER == "gemini":
        try:
            from google import genai
            class GeminiLLMAdapter(BaseLLMAdapter):
                def __init__(self):
                    self.client = genai.Client(api_key=AgentConfig.LLM_API_KEY)
                def generate(self, prompt: str) -> str:
                    try:
                        response = self.client.models.generate_content(
                            model='gemini-flash-latest',
                            contents=prompt
                        )
                        return response.text
                    except Exception as e:
                        print(f"Error con Gemini API: {e}")
                        return MockLLMAdapter().generate(prompt)
            return GeminiLLMAdapter()
        except ImportError:
            # Fallback si no está instalada la librería
            return MockLLMAdapter()
            
    # Fallback por defecto
    return MockLLMAdapter()
