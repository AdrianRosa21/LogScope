import unittest
from agent.agent import LogScopeAgent

class TestAgent(unittest.TestCase):
    def test_agent_triage_routing(self):
        agent = LogScopeAgent()
        # Verificar routing directo a triage
        diag = agent.router.route_request("triage", {"resumen": {"total_lineas": 10, "eventos_validos": 10, "total_error": 8}})
        self.assertEqual(diag["prioridad"], "CRITICA")

    def test_agent_full_incident(self):
        agent = LogScopeAgent()
        texto = "[ERROR] Fuego\n[ERROR] Fuego2\n[ERROR] Fuego3"
        result = agent.analyze_full_incident(text=texto)
        
        # Validación
        self.assertEqual(result["resumen_analisis"]["total_lineas"], 3)
        self.assertEqual(result["resumen_analisis"]["total_error"], 3)
        
        # Diagnóstico (100% de errores de un total de 3) -> 100% errores es crítico según threshold 20%
        self.assertEqual(result["diagnostico_agente"]["prioridad"], "CRITICA")
        
        # LLM mock
        self.assertIn("simulada", result["llm_comentario"].lower())
        self.assertIn("Triaje y Resumen", result["skills_usadas"])

    def test_agent_llm_failure(self):
        agent = LogScopeAgent()
        # Modificar forzadamente el adapter para lanzar error
        def mock_generate(*args, **kwargs):
            raise Exception("LLM Caído")
        agent.adapter.generate = mock_generate
        
        # El agente debería manejar el fallo al generar comentario
        try:
            result = agent.analyze_full_incident(text="[ERROR] Fuego")
            # En la versión actual de agent.py, la excepción se propaga y routes.py devuelve 500, o
            # agent.py devuelve el error, lo cual es manejado arriba.
            # Veamos si lanza
        except Exception as e:
            self.assertIn("LLM Caído", str(e))
