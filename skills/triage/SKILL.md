---
name: Triaje y Resumen de Incidentes
description: Clasifica un incidente de logs y genera un resumen con hechos, inferencias y recomendaciones basado en una matriz de triaje.
---

# Skill: Triaje y Resumen de Incidentes

## Responsabilidad
- Recibir el resumen estructurado de los logs (de validation skill o directamente del frontend).
- Identificar patrones relevantes y asignar una prioridad (BAJA, MEDIA, ALTA, CRITICA) de manera determinista.
- Separar hechos observados, inferencias y recomendaciones.
- Indicar falta de evidencia si el log está vacío.

## Cuándo debe activarse
- Cuando el usuario pida un diagnóstico global, un resumen, o un análisis de la gravedad del sistema.

## Entradas
- `resumen_serializado`: Diccionario emitido por el servicio de análisis o la skill de validación.

## Salidas
Diccionario con la prioridad y listas estructuradas para hechos, inferencias y recomendaciones.
