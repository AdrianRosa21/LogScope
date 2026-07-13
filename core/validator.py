from datetime import datetime
from core.models import ResultadoLinea
from core.parser import extraer_componentes, parece_fecha

def es_fecha_valida(cadena_fecha: str) -> bool:
    """
    Comprueba si una fecha en formato YYYY-MM-DD existe realmente en el calendario.
    """
    try:
        datetime.strptime(cadena_fecha, "%Y-%m-%d")
        return True
    except ValueError:
        return False

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
