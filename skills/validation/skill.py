from application.analysis_service import analizar_texto, analizar_archivo, serializar_resumen

def validate_logs(text: str = None, filepath: str = None) -> dict:
    """
    Ejecuta el núcleo determinista de validación sobre el texto o archivo indicado.
    Devuelve el resultado estructurado.
    """
    if filepath:
        resumen = analizar_archivo(filepath)
    elif text:
        resumen = analizar_texto(text)
    else:
        raise ValueError("Se debe proporcionar 'text' o 'filepath'")
        
    return serializar_resumen(resumen)
