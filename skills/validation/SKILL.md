---
name: Validación Estructurada de Logs
description: Procesa texto en bruto o archivos usando el motor determinista de LogScope.
---

# Skill: Validación Estructurada de Logs

## Responsabilidad
- Recibir texto, líneas o una ruta permitida.
- Ejecutar el núcleo determinista.
- Devolver un resultado estructurado.
- No utilizar el LLM para validar.
- Incluir números de línea y evidencia original.

## Cuándo debe activarse
- Cuando el usuario proporciona un nuevo bloque de texto de logs y solicita validarlo.
- Cuando el sistema frontend sube un archivo y se requiere analizar su validez.

## Cuándo no debe activarse
- Cuando los logs ya fueron validados y el usuario solo pide explicaciones o resúmenes.

## Entradas
- `text` (opcional): Texto en bruto con líneas de logs.
- `filepath` (opcional): Ruta al archivo a validar.

## Salidas
Un diccionario con:
- `total_lineas`, `eventos_validos`, `malformados`.
- `resultados`: Lista de objetos que contienen `numero_linea`, `es_valida`, `motivo_error`, etc.

## Restricciones
- El LLM NO debe inferir la validez. Debe usar esta herramienta obligatoriamente.
