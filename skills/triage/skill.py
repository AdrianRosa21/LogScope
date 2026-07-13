import json
import os

def load_triage_matrix() -> dict:
    path = os.path.join(os.path.dirname(__file__), "resources", "triage_matrix.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def summarize_incidents(resumen_serializado: dict) -> dict:
    """
    Recibe el resumen estructurado, identifica patrones y calcula una prioridad
    usando las reglas transparentes de la matriz de triaje.
    """
    matrix = load_triage_matrix()
    
    total = resumen_serializado.get("total_lineas", 0)
    validos = resumen_serializado.get("eventos_validos", 0)
    errores = resumen_serializado.get("total_error", 0)
    warnings = resumen_serializado.get("total_warning", 0)
    malformados = resumen_serializado.get("malformados", 0)
    
    if total == 0:
        return {
            "prioridad": "BAJA",
            "hechos": ["El archivo o texto está vacío o no pudo ser leído."],
            "inferencias": ["No hay actividad registrada en los logs proporcionados."],
            "recomendaciones": ["Verificar la fuente de los logs y asegurar que el sistema esté emitiendo registros."],
            "falta_evidencia": True
        }
    
    pct_errores = (errores / validos) * 100 if validos > 0 else 0
    pct_malformados = (malformados / total) * 100
    
    prioridad = "BAJA"
    if pct_errores >= matrix["critical"]["error_threshold_pct"] or errores >= matrix["critical"]["error_threshold_count"]:
        prioridad = "CRITICA"
    elif pct_errores >= matrix["alta"]["error_threshold_pct"] or errores >= matrix["alta"]["error_threshold_count"]:
        prioridad = "ALTA"
    elif warnings >= matrix["media"]["warning_threshold_count"] or pct_malformados >= matrix["media"]["malformed_threshold_pct"]:
        prioridad = "MEDIA"
        
    hechos = [
        f"Se procesaron {total} líneas en total.",
        f"Se encontraron {errores} errores y {warnings} advertencias.",
        f"Hay {malformados} líneas con estructura malformada."
    ]
    
    inferencias = []
    if prioridad == "CRITICA":
        inferencias.append("La alta cantidad de errores sugiere una posible falla sistémica o interrupción de servicio.")
    elif prioridad == "ALTA":
        inferencias.append("Los errores presentes requieren atención para prevenir fallas mayores.")
    elif prioridad == "MEDIA":
        inferencias.append("El sistema presenta inestabilidad menor o logs ruidosos (malformados/warnings).")
    else:
        inferencias.append("El sistema parece operar con normalidad basándose en la baja tasa de errores.")
        
    recomendaciones = []
    if malformados > 0:
        recomendaciones.append("Revisar la configuración de los emisores de log para corregir las líneas malformadas.")
    if errores > 0:
        recomendaciones.append("Investigar los mensajes de ERROR específicos para identificar la causa raíz.")
    if prioridad in ["ALTA", "CRITICA"]:
        recomendaciones.append("Escalar este incidente al equipo de guardia inmediatamente.")
        
    return {
        "prioridad": prioridad,
        "hechos": hechos,
        "inferencias": inferencias,
        "recomendaciones": recomendaciones,
        "falta_evidencia": False
    }
