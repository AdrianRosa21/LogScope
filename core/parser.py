import re
from typing import Optional, Dict

# Expresión regular principal para extraer severidad, fecha (opcional) y mensaje.
# Utilizamos re.IGNORECASE para que info, WARNING, [error] coincidan.
REGEX_LINEA = re.compile(
    r"^\[?(INFO|WARNING|ERROR)\]?\s+(?:(\d{4}-\d{2}-\d{2})\s+)?(.+)$", 
    re.IGNORECASE
)

# Expresión regular secundaria para detectar si el mensaje comienza con una fecha malformada.
# Nos ayuda a identificar el caso límite "Fecha con formato incorrecto".
REGEX_PARECE_FECHA = re.compile(r"^\d{4}[-/]\d{2}[-/]\d{2}")

def parece_fecha(texto: str) -> bool:
    """
    Verifica si un fragmento de texto comienza con algo que parece una fecha,
    incluso si tiene un formato incorrecto (ej. barras en lugar de guiones).
    """
    return bool(REGEX_PARECE_FECHA.match(texto))

def extraer_componentes(linea: str) -> Optional[Dict[str, str]]:
    """
    Aplica la expresión regular principal a la línea y devuelve un diccionario
    con sus partes. Devuelve None si la estructura base no coincide.
    """
    match = REGEX_LINEA.match(linea)
    if not match:
        return None
    
    return {
        "severidad": match.group(1).upper(),
        "fecha": match.group(2),
        "mensaje": match.group(3)
    }
