import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

class AgentConfig:
    LLM_API_KEY = os.getenv("LLM_API_KEY", "")
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "mock") # "mock" para pruebas
    AGENT_NAME = "LogScopeAgent"
    ROLE = "Analista técnico de logs especializado en explicación, triaje y recomendaciones basadas en evidencia"
