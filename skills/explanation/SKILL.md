---
name: Explicación de Líneas Malformadas
description: Explica por qué una línea específica fue rechazada por el validador, dando una posible solución.
---

# Skill: Explicación de Líneas Malformadas

## Responsabilidad
- Recibir exclusivamente resultados generados por el núcleo (número de línea, texto, motivo).
- Explicar de forma sencilla por qué la línea es inválida.
- Citar el número de línea.
- Indicar una posible corrección.
- No inventar campos faltantes ni cambiar el resultado.

## Cuándo debe activarse
- Cuando el usuario pregunte por qué falló una línea en particular o solicite ayuda para arreglarla.

## Entradas
- `texto_original`: El string original de la línea fallida.
- `motivo_error`: La cadena de error generada por el `validator.py`.
- `numero_linea`: El entero correspondiente a la línea en el archivo original.

## Salidas
Un diccionario con la explicación y una sugerencia de corrección.
