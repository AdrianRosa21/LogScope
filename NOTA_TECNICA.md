# Nota Técnica: Refactorización de LogScope

## 1. Problemas Originales Detectados
- **Monolito de Análisis**: El archivo `analyzer.py` combinaba la lectura de archivos I/O, el parseo de regex y la lógica de validación (fechas y estructura). Además, suprimía silenciosamente las excepciones (`except Exception: pass`).
- **Archivos Temporales Innecesarios**: El endpoint de texto en `main.py` escribía el texto en disco como un archivo `.txt` temporal para reutilizar `analizar_archivo`, lo cual era ineficiente y riesgoso.
- **Acoplamiento Web**: `main.py` mezclaba la configuración, las rutas de Flask y la inicialización, dificultando su testabilidad (falta de App Factory).

## 2. Refactorizaciones Realizadas
Se implementó una arquitectura limpia con las siguientes capas:
- **Core (Dominio)**: Separado en `models.py`, `parser.py`, `validator.py` y `exceptions.py`. Ahora la validación no sabe nada sobre los archivos.
- **Application**: Se creó `analysis_service.py` que centraliza la orquestación del análisis (tanto texto en memoria como archivos en disco) y la serialización JSON.
- **Web**: Se introdujo el patrón App Factory (`__init__.py`) y los endpoints se aislaron usando Blueprints (`routes.py`).
- **Agent & Skills**: Se crearon carpetas dedicadas. El Agente usa un Router y las Skills están aisladas con su respectivo `SKILL.md`.

## 3. Justificación de Decisiones
- **Separación Lógica / Configuración**: Al sacar la serialización hacia `application` y el setup hacia `web`, `core` queda exclusivamente enfocado en las reglas de negocio deterministas dictadas por el problema original.
- **Agente sin dependencias bloqueantes**: Se implementó un LLM Adapter con un proveedor `mock` (simulado) por defecto para que las pruebas unitarias y la ejecución pasen sin requerir configurar API keys, cumpliendo con la rúbrica sobre dependencias de conexión externa.

## 4. Personalización del Agente y Skills
Se crearon tres skills:
1. **Validación**: Encapsula el núcleo de análisis determinista sin usar IA (manteniendo la filosofía "IA como herramienta").
2. **Explicación**: Proporciona sugerencias claras para cada tipo de error.
3. **Triaje**: Genera un diagnóstico basado en los conteos de severidades mediante umbrales claros.

El agente `LogScopeAgent` coordina de manera centralizada estas skills a través de su `SkillRouter`.

## 5. Limitaciones y Mejoras
- **Limitación**: El frontend envía el JSON al endpoint de triaje en lugar de mandar todo el texto al agente, para ahorrar proceso y tokens LLM. Si se requiriera un análisis semántico de los mensajes, el agente tendría que leer las líneas individuales.
- **Posible mejora**: Añadir una base de datos vectorial para que la skill de explicación provea soluciones documentadas (ej. RAG) en base a errores previos.
