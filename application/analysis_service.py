import os
from typing import List
from core.models import ResumenAnalisis
from core.validator import analizar_linea
from core.exceptions import FileEncodingError, InvalidFileExtensionError

def _analizar_lineas(lineas: List[str]) -> ResumenAnalisis:
    resumen = ResumenAnalisis()
    for i, linea in enumerate(lineas, start=1):
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
    return resumen

def analizar_texto(texto: str) -> ResumenAnalisis:
    """
    Analiza un texto en memoria sin necesidad de escribir archivos.
    """
    if not texto:
        return ResumenAnalisis()
    lineas = texto.splitlines(keepends=True)
    return _analizar_lineas(lineas)

def analizar_archivo(ruta_archivo: str) -> ResumenAnalisis:
    """
    Lee un archivo línea por línea en UTF-8 y consolida el ResumenAnalisis.
    Lanza excepciones si hay problemas de extensión o codificación.
    """
    if not ruta_archivo or not os.path.exists(ruta_archivo) or not os.path.isfile(ruta_archivo):
        return ResumenAnalisis()
        
    if not ruta_archivo.lower().endswith(".txt"):
        raise InvalidFileExtensionError("Solo se permiten archivos .txt.")

    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            # Iterar directamente es más seguro para archivos grandes
            return _analizar_lineas(archivo)
    except UnicodeDecodeError:
        raise FileEncodingError("El archivo no tiene una codificación UTF-8 válida.")

def serializar_resumen(resumen: ResumenAnalisis) -> dict:
    """Convierte el objeto ResumenAnalisis a un dict serializable en JSON"""
    resultados_list = []
    for r in resumen.resultados:
        resultados_list.append({
            'numero_linea': r.numero_linea,
            'es_valida': r.es_valida,
            'severidad': r.severidad if r.severidad else "-",
            'fecha': r.fecha.strftime("%Y-%m-%d") if r.fecha else "-",
            'tiene_fecha': r.tiene_fecha,
            'mensaje': r.mensaje if r.mensaje else "-",
            'motivo_error': r.motivo_error if r.motivo_error else "",
            'texto_original': r.texto_original
        })
        
    return {
        'total_lineas': resumen.total_lineas,
        'eventos_validos': resumen.eventos_validos,
        'total_info': resumen.total_info,
        'total_warning': resumen.total_warning,
        'total_error': resumen.total_error,
        'malformados': resumen.total_lineas - resumen.eventos_validos,
        'resultados': resultados_list
    }

