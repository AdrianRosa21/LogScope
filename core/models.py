from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

@dataclass
class ResultadoLinea:
    """
    Representa el resultado del análisis de una única línea del log.
    
    Almacena los datos originales, la información parseada y el
    estado de validación para desacoplar el núcleo de la vista.
    """
    numero_linea: int
    texto_original: str
    es_valida: bool
    severidad: Optional[str] = None
    fecha: Optional[datetime] = None
    tiene_fecha: bool = False
    mensaje: Optional[str] = None
    motivo_error: Optional[str] = None

@dataclass
class ResumenAnalisis:
    """
    Agrupa las estadísticas totales del texto o archivo procesado junto con
    la lista de todas las líneas analizadas.
    """
    total_lineas: int = 0
    eventos_validos: int = 0
    total_info: int = 0
    total_warning: int = 0
    total_error: int = 0
    resultados: List[ResultadoLinea] = field(default_factory=list)
