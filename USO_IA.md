# Uso Consciente de Inteligencia Artificial

## IA Utilizada como Asistente
Durante el desarrollo y la refactorización de este proyecto, se utilizó un asistente de IA (Antigravity) como copiloto arquitectónico.

## Decisiones No Delegadas
- **Filosofía Fundamental**: La IA **no** decide si una línea de log es válida o no. Esta decisión de diseño fue protegida rigurosamente. Las herramientas deterministas (Regex, `datetime.strptime`) siguieron siendo la única fuente de verdad para la validación de estructura.
- **Rutas y Estructura**: La decisión de cómo organizar el patrón de "Skills" y en qué directorios separar la lógica (Core, Application, Web, Agent) fue supervisada manualmente.
- **Silencio de Excepciones**: Se decidió manualmente remover el `except Exception: pass` heredado del código anterior, permitiendo a la API responder con errores 500 en lugar de comerse fallas de codificación.

## Sugerencias de IA
- **Sugerencias Aceptadas**:
  - Usar un patrón de App Factory y Blueprint de Flask para independizar `main.py`.
  - Crear un "Mock LLM Adapter" de forma que la automatización de pruebas y la ejecución local no colapse sin una API Key de OpenAI o Gemini.
  - Reutilizar la lógica de serialización para enviarla desde la capa Application tanto a los Web Endpoints como a las Skills.
  - Implementar un router explícito en lugar de un prompt monolítico, evitando que el LLM intente adivinar comandos Python.

- **Sugerencias Rechazadas por Rodrigo Rosa**:
  - Se rechazó la sugerencia de generar las explicaciones de líneas malformadas dinámicamente con el LLM, para garantizar determinismo y velocidad, limitando el rol del LLM a un "comentario" o resumen global.
  - Se rechazó reconstruir el Frontend desde cero con un framework moderno (ej. React) por ir en contra de la premisa de "no reemplazar ni reconstruir innecesariamente", lo que hubiera roto compatibilidad.

## Validaciones y Evidencias
- Se implementaron y corrieron 23 pruebas unitarias (`python -m unittest discover -v`), logrando un paso del 100%.
- La interfaz fue probada manualmente para asegurar mitigaciones de XSS (usando `textContent` en Javascript para poblar las respuestas del agente).
