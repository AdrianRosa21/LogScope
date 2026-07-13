import json
from agent.agent import LogScopeAgent

def run_test():
    texto = """[INFO] 2025-01-01 Sistema iniciado correctamente
[WARNING] 2025-01-01 La latencia de la base de datos es alta
[ERROR] 2025-01-01 Conexion rechazada por el servidor principal
[ERROR] 2025-01-01 Fallo en escritura de base de datos
"""
    print("Iniciando LogScopeAgent con Gemini...")
    agent = LogScopeAgent()
    resultado = agent.analyze_full_incident(text=texto)
    
    print("\n=== RESUMEN DETERMINISTA ===")
    print(json.dumps(resultado["resumen_analisis"], indent=2, ensure_ascii=False))
    
    print("\n=== DIAGNOSTICO DEL AGENTE ===")
    print(json.dumps(resultado["diagnostico_agente"], indent=2, ensure_ascii=False))
    
    print("\n=== COMENTARIO GENERADO POR GEMINI ===")
    print(resultado["llm_comentario"])
    
if __name__ == "__main__":
    run_test()
