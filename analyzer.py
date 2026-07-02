import os
import re
from datetime import datetime
from models import ResumenAnalisis, ResultadoLinea

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

def es_fecha_valida(cadena_fecha: str) -> bool:
    """
    Comprueba si una fecha en formato YYYY-MM-DD existe realmente en el calendario.
    """
    try:
        datetime.strptime(cadena_fecha, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def extraer_componentes(linea: str) -> dict:
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

def analizar_linea(linea: str, numero_linea: int) -> ResultadoLinea:
    """
    Analiza una sola línea aplicando las reglas de negocio dictadas en DECISIONES.md.
    Construye y devuelve un objeto ResultadoLinea.
    """
    # 1. Línea vacía
    linea_limpia = linea.strip()
    if not linea_limpia:
        return ResultadoLinea(
            numero_linea=numero_linea,
            texto_original=linea,
            es_valida=False,
            motivo_error="Línea vacía"
        )
    
    # 2. Extracción de componentes
    componentes = extraer_componentes(linea_limpia)
    if not componentes:
        return ResultadoLinea(
            numero_linea=numero_linea,
            texto_original=linea,
            es_valida=False,
            motivo_error="Estructura inválida, severidad desconocida o falta mensaje"
        )
    
    severidad = componentes["severidad"]
    fecha_str = componentes["fecha"]
    mensaje = componentes["mensaje"]
    
    # 3. Detectar fecha con formato incorrecto
    # Si la regex no capturó fecha (porque no era YYYY-MM-DD), pero el mensaje empieza con algo parecido
    if not fecha_str and parece_fecha(mensaje):
        return ResultadoLinea(
            numero_linea=numero_linea,
            texto_original=linea,
            es_valida=False,
            motivo_error="Fecha con formato incorrecto"
        )
    
    # DECISIÓN CLAVE: Validar que la fecha sea real con datetime. 
    # Usar solo Regex permitiría pasar "2025-02-30". El estudiante forzó el uso del calendario.
    # 4. Validar que la fecha sea real
    fecha_obj = None
    tiene_fecha = False
    
    if fecha_str:
        if not es_fecha_valida(fecha_str):
            return ResultadoLinea(
                numero_linea=numero_linea,
                texto_original=linea,
                es_valida=False,
                motivo_error="Fecha imposible (no existe en el calendario)"
            )
        fecha_obj = datetime.strptime(fecha_str, "%Y-%m-%d")
        tiene_fecha = True
        
    # 5. Línea completamente válida
    return ResultadoLinea(
        numero_linea=numero_linea,
        texto_original=linea,
        es_valida=True,
        severidad=severidad,
        fecha=fecha_obj,
        tiene_fecha=tiene_fecha,
        mensaje=mensaje
    )

def analizar_archivo(ruta_archivo: str) -> ResumenAnalisis:
    """
    DECISIÓN CLAVE: El analizador es 100% independiente de la UI (Cero acoplamiento).
    Lee un archivo línea por línea en UTF-8 y consolida el ResumenAnalisis.
    Maneja excepciones de ruta y codificación regresando conteos limpios.
    """
    resumen = ResumenAnalisis()
    
    # Validaciones rápidas de archivo (rutas inexistentes o vacías)
    if not ruta_archivo or not os.path.exists(ruta_archivo) or not os.path.isfile(ruta_archivo):
        return resumen
        
    if not ruta_archivo.lower().endswith(".txt"):
        return resumen

    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            for i, linea in enumerate(archivo, start=1):
                resumen.total_lineas += 1
                resultado = analizar_linea(linea, i)
                resumen.resultados.append(resultado)
                
                if resultado.es_valida:
                    resumen.eventos_validos += 1
                    if resultado.severidad == "INFO":
                        resumen.total_info += 1
                    elif resultado.severidad == "WARNING":
                        resumen.total_warning += 1
                    elif resultado.severidad == "ERROR":
                        resumen.total_error += 1
                        
    except Exception:
        # En caso de error de lectura grave (ej. no es UTF-8 real) 
        # devolvemos el resumen con lo que se haya podido leer hasta el fallo.
        pass
        
    return resumen
