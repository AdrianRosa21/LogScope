from agent.config import AgentConfig
from agent.prompt import SYSTEM_PROMPT
from agent.adapter import get_llm_adapter
from agent.router import SkillRouter

class LogScopeAgent:
    def __init__(self):
        self.name = AgentConfig.AGENT_NAME
        self.role = AgentConfig.ROLE
        self.adapter = get_llm_adapter()
        self.router = SkillRouter()
        
    def analyze_full_incident(self, text: str = None, filepath: str = None) -> dict:
        """
        Composición ordenada de varias skills:
        1. Valida los logs (Validation)
        2. Resume y prioriza (Triage)
        3. Usa el adaptador LLM para un comentario final
        """
        # 1. Validación
        resumen = self.router.route_request("validate", {"text": text, "filepath": filepath})
        
        # 2. Triaje
        triaje = self.router.route_request("triage", {"resumen": resumen})
        
        # 3. LLM Mock Response
        # En una integración real, el agente inyectaría el prompt + triaje al LLM
        comentario = self.adapter.generate(f"{SYSTEM_PROMPT}\n\nDiagnóstico: {triaje}")
        
        return {
            "resumen_analisis": resumen,
            "diagnostico_agente": triaje,
            "llm_comentario": comentario,
            "skills_usadas": ["Validación Estructurada", "Triaje y Resumen"]
        }
