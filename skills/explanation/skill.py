def explain_malformed_line(texto_original: str, motivo_error: str, numero_linea: int) -> dict:
    """
    Recibe un resultado generado por el núcleo y explica por qué una línea es inválida.
    Devuelve la explicación, el número de línea y una posible corrección.
    Esta función no usa el LLM para validar, solo explica el error detectado determinísticamente.
    """
    explicacion = ""
    correccion = ""
    
    if "Línea vacía" in motivo_error:
        explicacion = "La línea no contiene caracteres visibles."
        correccion = "Eliminar la línea o introducir un registro válido (ej. [INFO] 2025-01-01 Mensaje)."
    elif "Estructura inválida" in motivo_error:
        explicacion = "La línea no tiene la estructura básica requerida: [SEVERIDAD] YYYY-MM-DD Mensaje."
        correccion = "Asegurar que inicia con INFO, WARNING o ERROR, seguido opcionalmente de fecha y luego el mensaje."
    elif "Fecha con formato incorrecto" in motivo_error:
        explicacion = "La fecha parece estar presente pero no usa el formato esperado (YYYY-MM-DD)."
        correccion = "Cambiar separadores (como barras '/') por guiones '-' y mantener el formato Año-Mes-Día."
    elif "Fecha imposible" in motivo_error:
        explicacion = "La fecha tiene el formato correcto, pero no existe en el calendario real (ej. 30 de febrero)."
        correccion = "Proporcionar una fecha válida que sí exista en el calendario."
    else:
        explicacion = "La línea es inválida debido a un error de estructura no clasificado."
        correccion = "Revisar la sintaxis de la línea y ajustarla al formato estándar."
        
    return {
        "numero_linea": numero_linea,
        "texto_original": texto_original,
        "motivo_detectado": motivo_error,
        "explicacion": explicacion,
        "posible_correccion": correccion
    }
